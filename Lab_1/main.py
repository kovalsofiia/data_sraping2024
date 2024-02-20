from requests import get
import requests
from bs4 import BeautifulSoup
FILE_NAME = "Lab_1 copy/institutes.txt"
BASE_URL = "https://lpnu.ua/institutes"

# page_2 = get(BASE_URL, verify=False)
# print(page_2.status_code)
# print (page_2.text)

with open(FILE_NAME, "w", encoding="utf-8") as file:
    response_3 = requests.get(BASE_URL, verify=False)
    soup = BeautifulSoup(response_3.content, "html.parser")

    institutes_list = soup.find(class_="view-content") # шукає список усіх інститутів із їхніми підкафедри зі сторінки вищевказаної(загальний)
    institute_paragraphs = institutes_list.find_all(class_="item-list") # шукає для кожного інституту список кафедр(поокремо потім)

    for institute_paragraph in institute_paragraphs:
        institute_name = institute_paragraph.find('h3').get_text(strip=True, separator=" ") #назва інституту яка записана у h3
        institute_link_end = institute_paragraph.find('a').get("href") #посилання інституту
        file.write(f"\nНазва інституту: {institute_name}  - URL: https://lpnu.ua{institute_link_end}")
        cafedras_names = institute_paragraph.find_all('li') #список усіх кафедр
        for cafedra in cafedras_names:
            caf_name = cafedra.find('a').get_text(strip=True, separator=" ") #назва кафедри
            caf_link_end = cafedra.find('a').get("href") #посилання кафедри
            
            caf_page = get(f"https://lpnu.ua{caf_link_end}")
            soup = BeautifulSoup(caf_page.content, "html.parser")
            zav_caf = soup.find(class_="field--item").get_text(strip=True, separator=" ")
            file.write(f"\n{caf_name} ||| URL: https://lpnu.ua{caf_link_end} ||| \n{zav_caf} ")
    file.write("\n\n\n")
            
print("Done")

