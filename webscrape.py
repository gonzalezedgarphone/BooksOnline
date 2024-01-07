
from bs4 import BeautifulSoup
import requests

# Titles of Books - Travel Page
url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

image_content = soup.find_all('div', class_='image_container')

for content in image_content:
    img_tag = content.find('img')

    title = img_tag['alt']

    print(f'Book Title: {title}')

# End of Travel Titles

# Space
print("")

# Product information Table Extracted - Travel Page

url = "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

table_content = soup.find_all('table', class_='table table-striped')

# First Part of UPC,Product Type,Price,Tax,Availability,Number of reviews - Travel Page

for table in table_content:
    th_content = soup.find_all('th')
    for a in th_content:
        th_text = a.get_text()
        print(f'Prodcut information 1:{th_text} ')

# End of Fisrt part Product information

# Space
print("")

# Second part of UPC,Product Type,Price,Tax,Availability,Number of reviews - Travel Page
for table in table_content:
    td_content = soup.find_all('td')
    for b in td_content:
        td_text = b.get_text()
        print (f'Prodcut information 2: {td_text}')

# End of Second part of Product information

# Space
print("")

# Imgage URl Extracted - Travel Page
url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
image_content = soup.find_all('div', class_='image_container')

for content in image_content:
    img_tag = content.find('img')

    src_image = img_tag['src']
    clean_image = src_image.removeprefix('../../../../')
    base_url_image = 'http://books.toscrape.com/'
    url_image = f'{base_url_image}{clean_image}'
    print(f'Image Url: {url_image}')
# End of Image Url

# Space
print("")

# All Ratings Extracted - Book in Travel
rating_content = soup.find_all('p', class_='star-rating')

for rating in rating_content[:]:
    rating_text = rating.get('class')
    if 'star-rating' in rating_text:
        rating_text.remove('star-rating')
    for star in rating_text:
        print(f'Review rating: {star}')
# End of All Ratings