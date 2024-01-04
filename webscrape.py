
from bs4 import BeautifulSoup
import requests

# Travel Page Extracted all titles
url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

image_content = soup.find_all('div', class_='image_container')

for content in image_content:
    img_tag = content.find('img')

    title = img_tag['alt']

    print(f'Book Title: {title}')

# Product information Table Extracted - Travel Page

url = "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

table_content = soup.find_all('table', class_='table table-striped')

for table in table_content:
    table_info = table.get_text(separator="     ")
    print(table_info)



