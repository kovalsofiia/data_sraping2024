import scrapy
from bs4 import BeautifulSoup
from lab2.items import InstituteItem, DepartmentItem, StaffItem

class LpnuSpider(scrapy.Spider):
    name = "lpnu"
    allowed_domains = ["lpnu.ua"]
    start_urls = ["https://lpnu.ua/institutes"]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        institutes_list = soup.find(class_="view-content")
        institute_paragraphs = institutes_list.find_all(class_="item-list")
        
        if institute_paragraphs:
            # Проходимось по кожному інституту
            for institute_paragraph in institute_paragraphs:
                institute_name = institute_paragraph.find('h3').get_text(strip=True, separator=" ")
                institute_link_end = institute_paragraph.find('a').get("href")
                institute_url = f"https://lpnu.ua{institute_link_end}"

                
                # Запит на парсинг сторінки інституту, передаємо дані про інститут через мета
                yield scrapy.Request(
                    url=institute_url,
                    callback=self.parse_institute,
                    meta={"institute_name": institute_name, "institute_url": institute_url}
                )

    def parse_institute(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        dep_list = soup.find(class_="item-list")
        departments_names = dep_list.find_all('li')
        institute_name = response.meta["institute_name"]  # Отримуємо ім'я інституту з мета-даних
        institute_url = response.meta["institute_url"]
        institute_image_url = soup.find(class_="views-field views-field-field-logotype").find(class_="img-responsive", name= "img").get("src")
        full_image_url = f"https://lpnu.ua{institute_image_url}"
        
        yield InstituteItem(
            name=institute_name,
            url=institute_url,
            image_urls= [full_image_url]
            )
        
        if dep_list:
            for department in departments_names:
                dep_name = department.find('a').get_text(strip=True, separator=" ")
                dep_url = department.find('a').get("href")
                yield DepartmentItem(
                    name=dep_name,
                    url=dep_url,
                    institute=institute_name,  # Додаємо ім'я інституту до кожної кафедри
                )
                yield scrapy.Request(
                    # адреса сторінки, яку необхідно парсити
                    url=dep_url,
                    # метод для обробки результатів завантаження
                    callback=self.parse_department,
                    # передаємо дані про кафедру в функцію колбеку
                    meta={
                        "department": dep_name,
                        "institute": institute_name
                    }
                )
                
    def parse_department(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        zav_caf = soup.find(class_="field field--name-field-contact-person field--type-string field--label-hidden field--items").get_text(strip=True, separator=" ")
        yield StaffItem(
            name=zav_caf,
            department=response.meta.get("department"),
            institute=response.meta.get("institute"),
        )