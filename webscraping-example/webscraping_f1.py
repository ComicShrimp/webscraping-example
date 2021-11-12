from typing import List

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

YEAR = "2021"

DATASOURCES: dict = {
    "races": {
        "name": "Races",
        "url": f"https://www.formula1.com/en/results.html/{YEAR}/races.html",
        "columns": ["Grand Prix", "Date", "Winner", "Car", "Laps", "Time"],
    },
    "drivers": {
        "name": "Drivers",
        "url": f"https://www.formula1.com/en/results.html/{YEAR}/drivers.html",
        "columns": ["Pos", "Driver", "Nationality", "Car", "PTS"],
    },
    "teams": {
        "name": "Teams",
        "url": f"https://www.formula1.com/en/results.html/{YEAR}/team.html",
        "columns": ["Pos", "Team", "PTS"],
    },
    "fastest_laps": {
        "name": "Fastest Laps",
        "url": f"https://www.formula1.com/en/results.html/{YEAR}/fastest-laps.html",
        "columns": ["Grand Prix", "Driver", "Car", "Time"],
    },
}

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)


def __get_html_table(url: str) -> str:
    """
    Get html table from F1 site
    """
    driver.get(url)
    element = driver.find_element(By.XPATH, "//table[@class='resultsarchive-table']")
    html_content = element.get_attribute("outerHTML")

    return html_content


def get_data(url: str, columns: List[str]) -> pd.DataFrame:
    """
    Get data from stats table in F1 site
    """
    html_content = __get_html_table(url)

    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find(name="table")

    df_all_data = pd.read_html(str(table))[0]
    df_filtered = df_all_data[columns]

    return df_filtered


for source in DATASOURCES.items():
    print(f"\n{source[1]['name']}: \n")

    df_result = get_data(source[1]["url"], source[1]["columns"])
    print(df_result)

driver.quit()
