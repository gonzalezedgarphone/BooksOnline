
from bs4 import BeautifulSoup
import requests

url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

image_content = soup.find_all('div', class_='image_container')

for content in image_content:
    img_tag = content.find('img')

    title = img_tag['alt']

    print(f'Book Title: {title}')

