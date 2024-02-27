import scrapy
from bs4 import BeautifulSoup
from lab2.items import InstituteItem

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
            
            yield scrapy.Request(
                # адреса сторінки, яку необхідно парсити
                url=f"https://lpnu.ua{institute_link_end}",
                # метод для обробки результатів завантаження
                callback=self.parse_faculty,
                # передаємо дані про факультет в функцію колбеку
                meta={
                    "faculty": institute_name
                }
            )
            
    def parse_faculty(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        
        # для кожної кафедри у списку
        if dep_list:
            for li in dep_list.find_all("li"):
                # знаходимо текст безпосередньо в контенті елементу  a
                dep_name = li.a.find(string=True, recursive=False)
                # URL кафедри
                dep_url = f"https://uzhnu.edu.ua{li.a.get('href')}"
                # повертаємо дані про кафедру
                yield DepartmentItem(
                    name=dep_name,
                    url=dep_url,
                    # факультет дізнаємось із метаданих, переданих при запиті
                    faculty=response.meta.get("faculty")
                )
                # також повертаємо запит для запуска скрапінгу працівників на сторінці кафедри
                yield scrapy.Request(
                    # адреса сторінки, яку необхідно парсити
                    url=dep_url+"/staff",
                    # метод для обробки результатів завантаження
                    callback=self.parse_department,
                    # передаємо дані про кафедру в функцію колбеку
                    meta={
                        "department": dep_name
                    }
                )