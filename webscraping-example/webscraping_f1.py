import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

YEAR = "2021"

DATASOURCES = {
    "race": {
        "url": f"https://www.formula1.com/en/results.html/{YEAR}/races.html",
        "columns": ["Grand Prix", "Date", "Winner", "Car", "Laps", "Time"],
    },
    "drivers": {
        "url": f"https://www.formula1.com/en/results.html/{YEAR}/drivers.html",
        "columns": ["Pos", "Driver", "Nationality", "Car", "PTS"],
    },
    "team": {
        "url": f"https://www.formula1.com/en/results.html/{YEAR}/team.html",
        "columns": ["Pos", "Team", "PTS"],
    },
    "fastest_lap": {
        "url": f"https://www.formula1.com/en/results.html/{YEAR}/fastest-laps.html",
        "columns": ["Grand Prix", "Driver", "Car", "Time"],
    },
}

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

driver.get(DATASOURCES["fastest_lap"]["url"])

element = driver.find_element(By.XPATH, "//table[@class='resultsarchive-table']")

html_content = element.get_attribute("outerHTML")

driver.quit()

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find(name="table")

df_full_race = pd.read_html(str(table))[0].head(10)

print(df_full_race)
