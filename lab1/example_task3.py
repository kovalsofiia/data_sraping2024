from requests import get
from bs4 import BeautifulSoup


BASE_URL = "https://www.uzhnu.edu.ua"
URL = f"{BASE_URL}/uk/cat/faculty"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
page = get(URL, headers=HEADERS)
soup = BeautifulSoup(page.content,  "html.parser")
# елемент що має клас departments_unfolded
fac_list = soup.find(class_="departments_unfolded")
# для кожного дочірнього елемента li
for li in fac_list.find_all("li"):
    # дочірній елемент a
    a = li.find("a")
    # знаходимо текст безпосередньо в контенті елементу  a
    fac_name = a.find(string=True, recursive=False)
    # URL складається з базового, та відносного, який записано в атрибуті href
    fac_url = BASE_URL + a.get("href")

    print(f"Назва факультету: {fac_name}")
    print(f"URL: {fac_url}")

    #завантажуємо сторінку факультету
    fac_page = get(fac_url, headers=HEADERS)
    #знаходимо список кафедр
    soup = BeautifulSoup(fac_page.content,  "html.parser")
    dep_list = soup.find(class_="departments")
    #для кожної кафедри у списку
    for li in dep_list.find_all("li"):
        # знаходимо текст безпосередньо в контенті елементу  a
        dep_name = li.a.find(string=True, recursive=False)
        # URL складається з базового, та відносного, який записано в атрибуті href
        dep_url = BASE_URL + a.get("href")

        print(f"    Назва кафедри: {dep_name}")
        print(f"    URL: {dep_url}")
