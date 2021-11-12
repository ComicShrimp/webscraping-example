import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

URL = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"

option = Options()
# option.headless = True
driver = webdriver.Firefox(options=option)

driver.get(URL)
driver.implicitly_wait(10)  # in seconds

driver.find_element(
    By.XPATH, "//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']"
).click()

element = driver.find_element(By.XPATH, "//div[@class='nba-stat-table']//table")

html_content = element.get_attribute("outerHTML")

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find(name="table")

df_full = pd.read_html(str(table))[0].head(10)

df = df_full[["Unnamed: 0", "PLAYER", "TEAM", "PTS"]]
df.columns = ["pos", "player", "team", "total"]

print(df)

driver.quit()
