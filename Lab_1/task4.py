from requests import get
import requests
from bs4 import BeautifulSoup
# 4. Використовуючи бібліотеку Beautiful soap отримати список підрозділів та їх URL.
print(f"--------------------------Task 3---------------------------------------------------------")
response = requests.get('https://hsc.gov.ua/pro-gsc/kerivnitstvo-rsts-ta-tsts/', verify=False)
soup = BeautifulSoup(response.content, "html.parser")

centers_list = soup.find(class_="entry-content")
ul_elements = centers_list.find_all("ul")
for ul in ul_elements:
    li_elements = ul.find_all("li")
    for li in li_elements:
        center_name = li.get_text(strip=True, separator=" ")
        a_tag = li.find("a")
        if a_tag:
            center_link = a_tag.get("href")
        else:
            center_link = "No link available"
        print(f"Назва центру: {center_name}")
        print(f"URL: {center_link}")