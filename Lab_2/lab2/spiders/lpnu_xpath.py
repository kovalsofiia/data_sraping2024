import scrapy
from lab2.items import InstituteItem, DepartmentItem, StaffItem

class LpnuSpider(scrapy.Spider):
    name = "lpnu_xpath"
    allowed_domains = ["lpnu.ua"]
    start_urls = ["https://lpnu.ua/institutes"]
# назви інститутів
    def parse(self, response):
        institutes = response.xpath("//div[@class='view-content']//div[contains(@class, 'item-list')]")
        for institute in institutes:
            institute_name = institute.xpath(".//h3//text()").get().strip()
            institute_link = institute.xpath(".//a/@href").get()
            institute_url = response.urljoin(institute_link)

            yield InstituteItem(
                name=institute_name,
                url=institute_url
            )

            yield scrapy.Request(
                url=institute_url,
                callback=self.parse_institute,
                meta={"institute_name": institute_name}
            )

    def parse_institute(self, response):
        departments = response.xpath("//div[contains(@class, 'item-list')]//li")
        institute_name = response.meta["institute_name"]

        for department in departments:
            dep_name = department.xpath(".//a//text()").get().strip()
            dep_url = response.urljoin(department.xpath(".//a/@href").get())

            yield DepartmentItem(
                name=dep_name,
                url=dep_url,
                institute=institute_name
            )

            yield scrapy.Request(
                url=dep_url,
                callback=self.parse_department,
                meta={
                    "department": dep_name,
                    "institute": institute_name,
                }
            )

    def parse_department(self, response):
        zav_caf = response.xpath("//div[contains(@class, 'field--name-field-contact-person')]//text()").get().strip()
        yield StaffItem(
            name=zav_caf,
            department=response.meta.get("department"),
            institute=response.meta.get("institute")
        )
