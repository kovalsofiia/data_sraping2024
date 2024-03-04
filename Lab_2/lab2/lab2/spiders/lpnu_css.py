import scrapy
from lab2.items import InstituteItem, DepartmentItem, StaffItem

class LpnuSpider(scrapy.Spider):
    name = "lpnu_css"
    allowed_domains = ["lpnu.ua"]
    start_urls = ["https://lpnu.ua/institutes"]

    def parse(self, response):
        institutes = response.css('.view-content .item-list')

        for institute in institutes:
            institute_name = institute.css('h3 a::text').get().strip()
            institute_url = response.urljoin(institute.css('h3 a::attr(href)').get())

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
        departments = response.css('.item-list > ul > li')
        institute_name = response.meta["institute_name"]

        for department in departments:
            dep_name = department.css('a::text').get().strip()
            dep_url = response.urljoin(department.css('a::attr(href)').get())

            yield DepartmentItem(
                name=dep_name,
                url=dep_url,
                institute=institute_name
            )

            # Requesting the department page for further parsing
            yield scrapy.Request(
                url=dep_url,
                callback=self.parse_department,
                meta={
                    "department": dep_name,
                    "institute": institute_name,
                }
            )

    def parse_department(self, response):
        # Extracting the head of department's name
        zav_caf = response.css('.field--name-field-contact-person::text').get().strip()

        yield StaffItem(
            name=zav_caf,
            department=response.meta.get("department"),
            institute=response.meta.get("institute")
        )
