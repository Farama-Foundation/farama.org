import os
import datetime
import requests
from bs4 import BeautifulSoup
import yaml
from yaml.loader import SafeLoader


DOWNLOADS_URL = "https://www.pepy.tech/projects/{pip_project}"
COLABTORATORS_URLS = (
    "https://api.github.com/repos/Farama-Foundation/{repo}/contributors"
)
REPOS_URLS = "https://api.github.com/repos/Farama-Foundation/{repo}"
REPOS_USE_URLS = "https://github.com/Farama-Foundation/{repo}/network/dependents"
GYM_REPOS_USE_URLS = "https://github.com/openai/gym/network/dependents"

SUBSUMED_PACKAGES = ["gym", "babyai", "gym-minigrid", "magent", "mo-gym"]


def scrape_project_downloads(project):
    project_downloads = 0
    try:
        soup = BeautifulSoup(
            requests.get(DOWNLOADS_URL.format(pip_project=project)).text, "html.parser"
        )
        project_downloads = str(soup).split('\\"totalDownloads\\":')[1].split(',')[0]
        project_downloads = int(project_downloads)
    except Exception as e:
        print(
            "Error while requesting data from: "
            f"{DOWNLOADS_URL.format(pip_project=project)}. This might mean"
            "that something changed in the API or the API is not public anymore."
        )
        print("Error message:")
        print(e)
    return project_downloads


def scrape_downloads(projects):
    total = 0
    res_dict = {}

    for project in SUBSUMED_PACKAGES:
        project_downloads = scrape_project_downloads(project)
        total += project_downloads
        res_dict[project] = project_downloads

    for project in projects:
        project_downloads = scrape_project_downloads(project["pip"])
        total += project_downloads
        res_dict[project["repo"]] = project_downloads

    print(f"Downloads: {res_dict}")
    return res_dict, total


def scrape_stars(projects):
    res_dict = {}
    total = 0

    for project in projects:
        project = project["repo"]
        res = requests.get(REPOS_URLS.format(repo=project))
        res_json = res.json()
        project_stars = (
            res_json["stargazers_count"]
            if "stargazers_count" not in res_json.keys()
            else 0
        )
        total += project_stars
        res_dict[project] = project_stars
    print(f"Stars: {res_dict}")
    return res_dict, total


def scrape_colaborators(projects):
    res_dict = {}
    MAX_PER_PAGE = 100
    usernames = []

    for project in projects:
        project = project["repo"]
        lastPage = False
        page = 1
        project_colaborators = 0

        while not lastPage:
            res = requests.get(
                COLABTORATORS_URLS.format(repo=project)
                + f"?per_page={MAX_PER_PAGE}&page={page}"
            )
            contributors = res.json()

            if len(contributors) == 0:
                break

            if len(contributors) < MAX_PER_PAGE:
                lastPage = True

            for contributor in contributors:
                project_colaborators += 1
                if contributor["login"] not in usernames:
                    usernames.append(contributor["login"])
            page += 1

        res_dict[project] = project_colaborators

    print(f"Colaborators: {res_dict}")
    return res_dict, len(usernames)


def retrieve_dependents_from_html(html):
    val = 0
    soup = BeautifulSoup(html, "html.parser")
    elem_selection = soup.select(
        "#dependents > div.Box > div.Box-header.clearfix > div > div.table-list-header-toggle.states.flex-auto.pl-0 > a.btn-link.selected"
    )
    if len(elem_selection) > 0:
        tmp_val = (
            elem_selection[0]
            .text.strip()
            .replace("Repositories", "")
            .replace(",", "")
            .rstrip()
        )
        val = int(tmp_val)
    return val


def find_package_id(html, pip_name):
    """Return the GitHub dependents package_id whose dropdown label matches the
    given PyPI package name, or None if there is no dropdown / no match.

    GitHub's "Used by" page can track several packages per repo (the PyPI
    package plus GitHub-repository packages, often inherited from a pre-fork
    history). Without a package_id GitHub shows a default that is sometimes the
    wrong one with 0 dependents. The PyPI package appears in the selector as a
    bare name (e.g. "highway-env"), while repository packages are prefixed with
    "github.com/", so matching the bare name against the pip name selects the
    correct package.
    """
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.select("a.select-menu-item"):
        text_el = item.select_one(".select-menu-item-text")
        if text_el is None:
            continue
        if text_el.text.strip().lower() == pip_name.lower():
            href = item.get("href", "")
            if "package_id=" in href:
                return href.split("package_id=")[1].split("&")[0]
    return None


def scrape_repos_use(projects):
    res_dict = {}
    total = 0
    for project in projects:
        repo = project["repo"]
        pip = project["pip"]
        try:
            url = REPOS_USE_URLS.format(repo=repo)
            res = requests.get(url)
            package_id = find_package_id(res.content, pip)
            if package_id:
                res = requests.get(f"{url}?package_id={package_id}")
            project_repos_use = retrieve_dependents_from_html(res.content)
            total += project_repos_use
            res_dict[repo] = project_repos_use
        except Exception as e:
            print(
                f"Unable to retrieve the number of dependent repositories at {REPOS_USE_URLS.format(repo=repo)}. \
                This might mean that something has changed in the page we are trying to scrape. \
                Make sure you update the query accordingly."
            )
            print("Error message:")
            print(e)

    try:
        res = requests.get(GYM_REPOS_USE_URLS)
        package_id = find_package_id(res.content, "gym")
        if package_id:
            res = requests.get(f"{GYM_REPOS_USE_URLS}?package_id={package_id}")
        project_repos_use = retrieve_dependents_from_html(res.content)
        total += project_repos_use
        res_dict["gym"] = project_repos_use
    except Exception as e:
        print(
            f"Unable to retrieve the number of dependent repositories at {GYM_REPOS_USE_URLS}. \
            This might mean that something has changed in the page we are trying to scrape. \
            Make sure you update the query accordingly."
        )
        print("Error message:")
        print(e)
    print(f"Dependent Repos: {res_dict}")
    return res_dict, total


def parse_project(project):
    repo = project["github"].split("/")[-1]
    return {
        "repo": repo,
        "pip": project.get("pip", repo),
    }


def scrape_stats():
    current_date = str(datetime.date.today().strftime("%Y-%m"))
    stats = {}
    complete_stats = {}
    stats_yaml = os.path.join(os.path.dirname(__file__), "..", "_data", "stats.yml")
    complete_stats_yaml = os.path.join(
        os.path.dirname(__file__), "..", "_data", "complete_stats.yml"
    )

    with open(stats_yaml) as fp:
        stats = yaml.load(fp, SafeLoader) or {}

    with open(complete_stats_yaml) as fp:
        complete_stats = yaml.load(fp, SafeLoader) or {}

    projects = []
    projects_yaml = os.path.join(
        os.path.dirname(__file__), "..", "_data", "projects.yml"
    )
    with open(projects_yaml) as fp:
        projects = yaml.load(fp, SafeLoader)
        projects = list(map(lambda x: parse_project(x), projects))

    for key in ["downloads", "colaborators", "repos_use", "stars"]:
        scraped_val = None
        projects_val_dict = {}
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

        # project -> stats -> date -> val
        for project in projects_val_dict.keys():
            if project not in complete_stats.keys():
                complete_stats[project] = {}

            if key not in complete_stats[project].keys():
                complete_stats[project][key] = {}

            complete_stats[project][key][current_date] = projects_val_dict[project]

    with open(stats_yaml, "w") as fp:
        yaml.dump(stats, fp)

    with open(complete_stats_yaml, "w") as fp:
        yaml.dump(complete_stats, fp)


if __name__ == "__main__":
    scrape_stats()
