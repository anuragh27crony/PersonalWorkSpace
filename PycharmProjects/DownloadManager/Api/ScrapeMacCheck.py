import requests
from bs4 import BeautifulSoup

page = requests.post("https://control.teletrax.tv/directmaccheck.aspx?mac=0C23")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="ContentPlaceHolder1_ResultsTable")
# seven_day = soup.find(id="seven-day-forecast")
# forecast_items = seven_day.find_all(class_="tombstone-container")
# tonight = forecast_items[0]
# print(tonight.prettify())
table_content = seven_day.get_text()

stripped_content = list()
for line in table_content.split("\n"):
    if line.rstrip():
        stripped_content.append(line)

print(stripped_content[12:24])
