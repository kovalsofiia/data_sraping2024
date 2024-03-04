import scrapy
from bs4 import BeautifulSoup
from lab2.items import InstituteItem, DepartmentItem

class LpnuSpider(scrapy.Spider):
    name = "lpnu"
    allowed_domains = ["lpnu.ua"]
    # початкова адреса з якої буде подальший скрапінг відбуватись
    start_urls = ["https://lpnu.ua/institutes"]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        institutes_list = soup.find(class_="view-content") # шукає список усіх інститутів із їхніми підкафедри зі сторінки вищевказаної(загальний)
        institute_paragraphs = institutes_list.find_all(class_="item-list") # шукає для кожного інституту список кафедр(поокремо потім)
        
        for institute_paragraph in institute_paragraphs:
            institute_name = institute_paragraph.find('h3').get_text(strip=True, separator=" ") #назва інституту яка записана у h3
            institute_link_end = institute_paragraph.find('a').get("href") #посилання інституту
            yield InstituteItem(
                name=institute_name,
                url=f"https://lpnu.ua{institute_link_end}"
            )
            # тут я зупинилась і до цього місця все працює. тобто є: список інститутів та посилання на сайт.
            
        for institute_paragraph in institute_paragraphs:
            institute_link_end = institute_paragraph.find('a').get("href")
            yield scrapy.Request(
                # адреса сторінки, яку необхідно парсити
                url=f"https://lpnu.ua{institute_link_end}",
                # метод для обробки результатів завантаження
                callback=self.parse_faculty,
                # передаємо дані про факультет в функцію колбеку
                meta={"faculty": institute_name}
            )
            
            # працює: зайти на сайт кожного інституту і зберегти список назв кафедр + посилання на кожну кафедру. 

    def parse_faculty(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        dep_list = soup.find(class_="item-list")
        departments_names = dep_list.find_all('li') #список усіх кафедр
        # для кожної кафедри у списку
        if dep_list:
            for department in departments_names:
                dep_name = department.find('a').get_text(strip=True, separator=" ") # назва кафедри
                dep_url = department.find('a').get("href") # URL кафедри
                # повертаємо дані про кафедру
                yield DepartmentItem(
                    name=dep_name,
                    url=dep_url,
                )
                
# треба: зайти на сайт кожної кафедри та зберегти: дані про завідувача кафедри.  