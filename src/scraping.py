import time
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path

import traceback
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

HTML_RACE_DIR = Path("..", "data", "html", "race")


def scrape_kaisai_date(from_: str, to_: str) -> list[str]:
    """
    Scrape race dates from netkeiba.com calendar.

    Args:
        from_ (str): Start date in YYYY-MM format.
        to_ (str): End date in YYYY-MM format.

    Returns:
        list[str]: List of race dates in YYYYMMDD format.
    """
    kaisai_date_list = []
    for date in tqdm(pd.date_range(from_, to_, freq="MS")):
        year = date.year
        month = date.month
        url = f"https://race.netkeiba.com/top/calendar.html?year={year}&month={month}"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(url, headers=headers, verify=True)
            response.raise_for_status()
            html = response.content
            soup = BeautifulSoup(html, "html.parser")
            a_list = soup.find("table", class_="Calendar_Table").find_all("a")
            for a in a_list:
                kaisai_date = re.findall(r"kaisai_date=(\\d{8})", a["href"])[0]
                kaisai_date_list.append(kaisai_date)
        except Exception as e:
            print(f"Error occurred while scraping {url}: {e}")

    return kaisai_date_list


def scrape_race_id_list(kaisai_date_list: list[str]) -> list[str]:
    """
    Scrape race IDs for given race dates.

    Args:
        kaisai_date_list (list[str]): List of race dates in YYYYMMDD format.

    Returns:
        list[str]: List of race IDs.
    """
    options = Options()
    options.add_argument("--headless")
    driver_path = ChromeDriverManager().install()
    race_id_list = []

    with webdriver.Chrome(service=Service(driver_path), options=options) as driver:
        for kaisai_date in tqdm(kaisai_date_list):
            url = f"https://race.netkeiba.com/top/race_list.html?kaisai_date={kaisai_date}"
            try:
                driver.get(url)
                time.sleep(1)
                li_list = driver.find_elements(By.CLASS_NAME, "RaceList_DataItem")
                for li in li_list:
                    href = li.find_element(By.TAG_NAME, "a").get_attribute("href")
                    race_id = re.findall(r"race_id=(\\d{12})", href)[0]
                    race_id_list.append(race_id)
            except Exception as e:
                print(f"Error occurred while scraping {url}: {e}")

    return race_id_list


def scrape_html_race(race_id_list: list[str], save_dir: Path = HTML_RACE_DIR) -> list[Path]:
    """
    Scrape race HTML data and save to files.

    Args:
        race_id_list (list[str]): List of race IDs.
        save_dir (Path): Directory to save HTML files.

    Returns:
        list[Path]: List of saved file paths.
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    html_path_list = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for race_id in tqdm(race_id_list):
        filepath = save_dir / f"{race_id}.bin"
        if filepath.is_file():
            print(f"Skipped: {race_id}")
            continue

        url = f"https://db.netkeiba.com/race/{race_id}"
        try:
            response = requests.get(url, headers=headers, verify=True)
            response.raise_for_status()
            html = response.content
            with open(filepath, "wb") as f:
                f.write(html)
            html_path_list.append(filepath)
            time.sleep(1)
        except Exception as e:
            print(f"Error occurred while scraping {url}: {e}")

    return html_path_list
