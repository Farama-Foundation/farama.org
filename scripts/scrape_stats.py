import os
from bs4 import BeautifulSoup
import yaml
from yaml.loader import SafeLoader

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

DOWNLOADS_URL = "https://pepy.tech/project/gym"
COLABTORATORS_URL = "https://pepy.tech/project/gym"
REPOS_USE_URL = "https://pepy.tech/project/gym"

def scrape_downloads():
    driver.get(DOWNLOADS_URL)
    res = driver.find_element("#root > div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.jss15.css-834p59 > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-7.MuiGrid-grid-xl-4.css-k3wsr6 > div > div.MuiCardContent-root.css-1qw96cp > div > div:nth-child(4)")
    print(res)
    # print(resp.html.find("#root > div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.jss15.css-834p59 > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-7.MuiGrid-grid-xl-4.css-k3wsr6 > div > div.MuiCardContent-root.css-1qw96cp > div > div:nth-child(4)"))
    # res = soup.select("#root > div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.jss15.css-834p59 > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-7.MuiGrid-grid-xl-4.css-k3wsr6 > div > div.MuiCardContent-root.css-1qw96cp > div > div:nth-child(4)")
    # print(res)

def scrape_stats():
    stats = {}
    with open(os.path.join(os.path.dirname(__file__), "..", "_data", "stats.yml")) as fp:
        stats = yaml.load(fp, SafeLoader)
    print(stats)
    for key, val in stats.items():
        if key == "downloads":
            scraped_val = scrape_downloads()
            stats[key] = scraped_val or val
        elif key == "colaborators":
            pass
        elif key == "repos_use":
            pass
        else:
            print("Invalid stat key")



if __name__ == "__main__":
    scrape_stats()