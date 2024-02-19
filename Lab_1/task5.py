from requests import get
import requests
from bs4 import BeautifulSoup
# 5. Зберегти результати скрапінгу до текстового файлу.
FILE_NAME = "Lab_1/centers.txt"
with open(FILE_NAME, "w", encoding="utf-8") as file:
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
            file.write(f"Назва центру: {center_name} - URL: {center_link}")
            file.write("\n")