import os
import datetime
import requests
from bs4 import BeautifulSoup
import yaml
from yaml.loader import SafeLoader


GYM_DOWNLOADS_URL = "https://api.pepy.tech/api/v2/projects/gym"
DOWNLOADS_URL = "https://api.pepy.tech/api/v2/projects/{pip_project}"
COLABTORATORS_URLS = "https://api.github.com/repos/Farama-Foundation/{repo}/contributors"
REPOS_URLS = "https://api.github.com/repos/Farama-Foundation/{repo}"
REPOS_USE_URLS = "https://github.com/Farama-Foundation/{repo}/network/dependents"
GYM_REPOS_USE_URLS = "https://github.com/openai/gym/network/dependents"


def scrape_downloads(projects):
    total = 0
    res_dict = {}
    try:
        res_json = requests.get(GYM_DOWNLOADS_URL).json()
        total = int(res_json["total_downloads"])
        res_dict["gym"] = total
    except Exception as e:
        print(f"Error while requesting data from: {GYM_DOWNLOADS_URL}. This might mean" + \
                "that something changed in the API or the API is not public anymore.")
        print("Error message:")
        print(e)

    for project in projects:
        try:
            res_json = requests.get(DOWNLOADS_URL.format(pip_project=project)).json()
            if "total_downloads" in res_json.keys():
                project_downloads = int(res_json["total_downloads"])
                total += project_downloads
                res_dict[project] = project_downloads
        except Exception as e:
            print(f"Error while requesting data from: {DOWNLOADS_URL.format(pip_project=project)}. This might mean" + \
                    "that something changed in the API or the API is not public anymore.")
            print("Error message:")
            print(e)

    print(f"Downloads: {res_dict}")
    return res_dict, total


def scrape_stars(projects):
    res_dict = {}
    total = 0

    for project in projects:
        res = requests.get(REPOS_URLS.format(repo=project))
        project_stars = res.json()["stargazers_count"]
        total += project_stars
        res_dict[project] = project_stars
    print(f"Stars: {res_dict}")
    return res_dict, total


def scrape_colaborators(projects):
    res_dict = {}
    MAX_PER_PAGE = 100
    usernames = []

    for project in projects:
        lastPage = False
        page = 1
        project_colaborators = 0

        while not lastPage:
            res = requests.get(COLABTORATORS_URLS.format(repo=project) + f"?per_page={MAX_PER_PAGE}&page={page}")
            contributers = res.json()

            if len(contributers) == 0:
                break

            if len(contributers) < MAX_PER_PAGE:
                lastPage = True

            for contributer in contributers:
                project_colaborators += 1
                if contributer["login"] not in usernames:
                    usernames.append(contributer["login"])
            page += 1

        res_dict[project] = project_colaborators

    print(f"Colaborators: {res_dict}")
    return res_dict, len(usernames)


def retrieve_dependents_from_html(html):
    val = 0
    soup = BeautifulSoup(html, 'html.parser')
    elem_selection = soup.select('#dependents > div.Box > div.Box-header.clearfix > div > div.table-list-header-toggle.states.flex-auto.pl-0 > a.btn-link.selected')
    if len(elem_selection) > 0:
        tmp_val = elem_selection[0].text.strip().replace("Repositories", "").replace(",", "").rstrip()
        val = int(tmp_val)
    return val


def scrape_repos_use(projects):
    res_dict = {}
    total = 0
    for project in projects:
        try:
            res = requests.get(REPOS_USE_URLS.format(repo=project))
            project_repos_use = retrieve_dependents_from_html(res.content)
            total += project_repos_use
            res_dict[project] = project_repos_use
        except Exception as e:
            print(f"Unable to retrieve the number of dependent repositories at {REPOS_USE_URLS.format(repo=project)}. \
                This might mean that something has changed in the page we are trying to scrape. \
                Make sure you update the query accordingly.")
            print("Error message:")
            print(e)

    try:
        res = requests.get(GYM_REPOS_USE_URLS)
        project_repos_use = retrieve_dependents_from_html(res.content)
        total += project_repos_use
        res_dict["gym"] = project_repos_use
    except Exception as e:
        print(f"Unable to retrieve the number of dependent repositories at {GYM_REPOS_USE_URLS}. \
            This might mean that something has changed in the page we are trying to scrape. \
            Make sure you update the query accordingly.")
        print("Error message:")
        print(e)
    print(f"Dependent Repos: {res_dict}")
    return res_dict, total


def scrape_stats():

    current_date = str(datetime.date.today())
    stats = {}
    complete_stats = {}
    stats_yaml = os.path.join(os.path.dirname(__file__), "..", "_data", "stats.yml")
    complete_stats_yaml = os.path.join(os.path.dirname(__file__), "..", "_data", "complete_stats.yml")

    with open(stats_yaml) as fp:
        stats = yaml.load(fp, SafeLoader) or {}

    with open(complete_stats_yaml) as fp:
        complete_stats = yaml.load(fp, SafeLoader) or {}

    projects = []
    projects_yaml = os.path.join(os.path.dirname(__file__), "..", "_data", "projects.yml")
    with open(projects_yaml) as fp:
        projects = yaml.load(fp, SafeLoader)
        projects = list(map(lambda x: x["github"].split("/")[-1].rstrip("/"), projects))

    for key in ["downloads", "colaborators", "repos_use", "stars"]:
        try:
            if key == "downloads":
                projects_val_dict, scraped_val = scrape_downloads(projects)
            elif key == "colaborators":
                projects_val_dict, scraped_val = scrape_colaborators(projects)
            elif key == "repos_use":
                projects_val_dict, scraped_val = scrape_repos_use(projects)
            elif key == "stars":
                projects_val_dict, scraped_val = scrape_stars(projects)
            else:
                print("Invalid stat key")
        except Exception as e:
            print(f"Error while scraping for key: {key}")
            print("Error message:")
            print(e)

        stats[key] = scraped_val or stats[key]

        # stars -> project -> date -> val
        if key not in complete_stats.keys():
            complete_stats[key] = {}

        for project in projects_val_dict.keys():
            if project not in complete_stats[key].keys():
                complete_stats[key][project] = {}

            complete_stats[key][project][current_date] = projects_val_dict[project]

    print(complete_stats)

    with open(stats_yaml, "w") as fp:
        yaml.dump(stats, fp)

    with open(complete_stats_yaml, "w") as fp:
        yaml.dump(complete_stats, fp)


if __name__ == "__main__":
    scrape_stats()