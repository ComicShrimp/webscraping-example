import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

URL = "https://www.formula1.com/en/results.html"

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

driver.get(URL)
driver.implicitly_wait(10)

element = driver.find_element(By.XPATH, "//table[@class='resultsarchive-table']")

html_content = element.get_attribute("outerHTML")

driver.quit()

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find(name="table")

df_full = pd.read_html(str(table))[0].head(10)

df = df_full[["Grand Prix", "Date", "Winner", "Car", "Laps", "Time"]]

print(df)
