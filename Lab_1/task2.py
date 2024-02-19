from requests import get
# 2. Переконатись, що сторінки є статичними. Використовуючи бібліотеку requests завантажити сторінку зі списком та вивести в консоль.
print(f"--------------------------Task 2---------------------------------------------------------")
URL = "https://hsc.gov.ua/pro-gsc/kerivnitstvo-rsts-ta-tsts/"
page = get(URL, verify=False)
print(page.status_code)
print (page.text)