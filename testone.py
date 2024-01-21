from bs4 import BeautifulSoup
import requests
import time
import csv

timeout_seconds = 300  # Set the timeout to 5 minutes

start_time = time.time()

def products_links(page):
    url = f'http://books.toscrape.com/catalogue/page-{page}.html'
    page_content = requests.get(url).content

    soup = BeautifulSoup(page_content, 'html.parser')

    image_content = soup.find_all('div', class_='image_container')
    links = []

    for content in image_content:
        img_tag = content.find('a')
        src_image = img_tag['href']
        clean_image = src_image.removeprefix('../../../../')
        base_url_image = 'http://books.toscrape.com/catalogue/'
        url_image = f'{base_url_image}{clean_image}'
        links.append(url_image)

    return links


# Example usage for paginating through 50 pages:
all_links = []

for page_num in range(1, 2):  # Assuming pages are numbered from 1 to 2 for testing
    page_links = products_links(page_num)
    if not page_links:  # If page_links is empty
        print(f"No more pages found.")
        break

    all_links.extend(page_links)

    if time.time() - start_time > timeout_seconds:
        print(f"Timeout reached. Stopping.")
        break

all_data_dicts = []
# Extracting data from each link:
for test_link in all_links:
    page_response = requests.get(test_link)

    if page_response.status_code != 200:
        print(f"Error accessing {test_link}. Status code: {page_response.status_code}")
        continue  # Skip to the next link if th

    page_content = requests.get(test_link).content
    soup = BeautifulSoup(page_content, 'html.parser')
    title_content = soup.find('div', class_='col-sm-6 product_main')
    category_name = soup.find('ul', class_='breadcrumb')
    table_content = soup.find_all('table', class_='table table-striped')
    rating_content = soup.find('p', class_='star-rating')
    image_content = soup.find('div', class_='item active')
    product_description = soup.find_all('div', id='product_description')
    data_dict = {}
    data_dict['Product_page_url'] = test_link

    if title_content:
        title_tag = title_content.find('h1')
        if title_tag:
            data_dict['Book title'] = title_tag.text

    if category_name:
        category_home = category_name.find('a')
        category_type = category_home.findNext('a')
        category_title = category_type.findNext('a').text
        data_dict['Category'] = category_title

    if rating_content:
        rating_text = rating_content.get('class')
        if 'star-rating' in rating_text:
            rating_text.remove('star-rating')
            data_dict['Review Rating'] = rating_text[0]



    for table in table_content:
        th_content = table.find_all('th')
        td_content = table.find_all('td')

        for a, b in zip(th_content, td_content):
            th_text = a.get_text(strip=True)
            td_text = b.get_text(strip=True)

            # Add key-value pairs to the data dictionary
            data_dict[th_text] = td_text

        # Remove 'Tax' from the dictionary
        data_dict.pop('Tax', None)
        data_dict.pop('Product Type', None)
    for product in product_description:
        p_content = product.find_next('p')
        p_text = p_content.get_text()
        data_dict['Product Description'] = p_text

    if image_content:
        img_tag = image_content.find('img')
        if img_tag:
            src_image = img_tag['src']
            clean_image = src_image.removeprefix('../../../../')
            base_url_image = 'http://books.toscrape.com/'
            url_image = f'{base_url_image}{clean_image}'
            data_dict['Image URL'] = url_image
            print(url_image)
    all_data_dicts.append(data_dict)
fields = ['Product_page_url', 'Book title', 'Category', 'Review Rating', 'UPC', 'Price (excl. tax)',
              'Price (incl. tax)',
              'Availability', 'Number of reviews', 'Product Description', 'Image URL']

filename = "test_one_three.csv"

    # Wrap data_dict in a list
data_dicts = [data_dict]

with open(filename, 'w', newline='',) as csvfile:
        # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_NONNUMERIC)

        # writing headers (field names)
    writer.writeheader()

        # writing data rows
    writer.writerows(all_data_dicts)

    #Print or process the data dictionary for each link
    #print("Data Dictionary:", data_dict)
    #print("\n")  # Add a newline to separate information for each book
