import requests
from bs4 import BeautifulSoup
import time
import os
import pandas as pd

# Retries for page response
MAX_RETRIES = 15
# 40 Minutes timeout for program
TIMEOUT_SECONDS = 2400
# 10 Minutes time out response
PAGE_RESPONSE_TIMEOUT = 600
BASE_URL = 'http://books.toscrape.com/'


# Method for downloading book images with title and storing the images locally
def download_book_image(book_data, base_path='images/'):
    """
        Download book images with title and store them locally.

        Parameters:
        - book_data (dict): Dictionary containing book information.
        - base_path (str): Base path for storing images.

        Returns:
        None
        """
    try:
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        # Extract the image URL and book title from the provided book_data dictionary
        image_url = book_data.get('Image url')
        book_title = book_data.get('Book title')

        # Check if either image URL or book title is not found
        if not image_url or not book_title:
            print(f"Skipping book - Image URL or title not found.")
            return

        image_retries = 0

        while image_retries < MAX_RETRIES:
            try:
                # Send an HTTP GET request to the image URL and raise an error for non-OK responses
                response = requests.get(image_url, timeout=PAGE_RESPONSE_TIMEOUT)
                response.raise_for_status()
                print(f"Downloading image for '{book_title}': {image_url}")
                # Remove invalid characters from the book title
                valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

                # Clean the book title by replacing invalid characters with underscores
                book_title_cleaned = ''.join(c if c in valid_chars else '_' for c in book_title)

                # Create a filename with the base path and the cleaned book title with a .jpg extension
                filename = os.path.join(base_path, f"{book_title_cleaned}.jpg")

                # Open the file in binary write mode and write the image content to the file
                with open(filename, 'wb') as f:
                    f.write(response.content)

                # Break out of the retry loop if successful
                break

            except requests.exceptions.Timeout as e:
                print(f"Timeout error downloading image for '{book_title}': {e}")
                image_retries += 1
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image for '{book_title}': {e}")
                image_retries += 1

        if image_retries == MAX_RETRIES:
            print(f"Max image download retries reached for '{book_title}'. Skipping.")

    except requests.exceptions.Timeout as e:
        if isinstance(e, requests.exceptions.Timeout):
            print(f"Timeout error downloading image for '{book_title}': {e}")
        else:
            print(f"Error downloading image for '{book_title}': {e}")


# Function to extract links from page
def products_links(page):
    """
        Extract links from a specific page.

        Parameters:
        - page (int): Page number.

        Returns:
        list: List of image URLs.
        """
    url = f'http://books.toscrape.com/catalogue/page-{page}.html'
    page_content = requests.get(url).content
    soup = BeautifulSoup(page_content, 'html.parser')

    #  List to store image URLs
    links = []

    # Find all div elements with class 'image_container'
    image_content = soup.find_all('div', class_='image_container')

    # Iterate through 'image_container'
    for content in image_content:
        img_tag = content.find('a')
        src_image = img_tag['href']
        clean_image = src_image.removeprefix('../../../../')
        base_url_image = 'http://books.toscrape.com/catalogue/'

        # Complete image URL
        url_image = f'{base_url_image}{clean_image}'

        # Append image URL to the list of links
        links.append(url_image)

    # Return the list of image URLs
    return links

# Set the timeout to 15 minutes
timeout_seconds = TIMEOUT_SECONDS
# Record the current time when the scraping process starts
start_time = time.time()

# List to store all extracted links
all_links = []

# Loop to extract links from range of pages
for page_num in range(1, 51):

    # Call the 'products_links' function to get current page link
    page_links = products_links(page_num)

    # Check if there are no more links
    if not page_links:
        print(f"No more pages found.")
        break

    # Extend the 'all_links' list with the links retrieved from the current page
    all_links.extend(page_links)

    # Check if the time exceeds the timeout
    if time.time() - start_time > timeout_seconds:
        print(f"Timeout reached. Stopping.")
        break

# Stores all data_dict information in list
all_data_dicts = []

# Loop to process each link and extract book data
for test_link in all_links:
    print(f"Retrieving information from: {test_link}")
    retries = 0
    while retries < MAX_RETRIES:
        try:
            time.sleep(0.6)  # Add a 0.6-second delay
            session = requests.Session()
            page_response = session.get(test_link, timeout=PAGE_RESPONSE_TIMEOUT)

            break
        except requests.exceptions.ReadTimeout as e:
            print(f"Timeout error accessing {test_link}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {test_link}: {e}")
            retries += 1
            if retries == MAX_RETRIES:
                print(f"Max retries reached for {test_link}. Skipping.")
                break  # Break out of the retry loop if max retries reached
            continue  # Retry the current link

    # Condition to test link
    if page_response.status_code != 200:
        print(f"Error accessing {test_link}. Status code: {page_response.status_code}")
        continue

    # Dictionary to store book data for each link
    data_dict = {}

    # Creates a GET request to the URL and BeautifulSoup object to parse the HTML content
    page_content = requests.get(test_link).content
    soup = BeautifulSoup(page_content, 'html.parser')

    # Find the title content section in the HTML
    title_content = soup.find('div', class_='col-sm-6 product_main')
    if title_content:
        title_tag = title_content.find('h1')
        if title_tag:
            data_dict['Book title'] = title_tag.text

    # Find the category name section in the HTML
    category_name = soup.find('ul', class_='breadcrumb')
    if category_name:
        category_home = category_name.find('a')
        category_type = category_home.findNext('a')
        category_title = category_type.findNext('a').text

        # Store the category title in the data dictionary
        data_dict['Category'] = category_title

    # Find the rating content section in the HTML
    rating_content = soup.find('p', class_='star-rating')
    if rating_content:
        rating_text = rating_content.get('class')
        if 'star-rating' in rating_text:
            rating_text.remove('star-rating')

            # Store the review rating in the data dictionary
            data_dict['Review rating'] = rating_text[0]

    # Find all the tables with the specified class in the HTML
    table_content = soup.find_all('table', class_='table table-striped')

    # Iterate through each pair of 'th' and 'td' tags
    for table in table_content:
        th_content = table.find_all('th')
        td_content = table.find_all('td')

        for a, b in zip(th_content, td_content):
            th_text = a.get_text(strip=True)
            td_text = b.get_text(strip=True)

            # Store the information in the data dictionary
            data_dict[th_text] = td_text

        # Removes 'tax' and 'product type' from the data dictionary
        data_dict.pop('Tax', None)
        data_dict.pop('Product Type', None)
        data_dict.pop('Number of reviews', None)

        # Changes the names of the previous keys to new ones
        data_dict['Price excluding tax'] = data_dict.pop('Price (excl. tax)')
        data_dict['Universal product code(upc)'] = data_dict.pop('UPC')
        data_dict['Price including tax'] = data_dict.pop('Price (incl. tax)')
        data_dict['Quantity available'] = data_dict.pop('Availability')

    # Finds all product description sections
    product_description = soup.find_all('div', id='product_description')

    # Iterate through each product description
    for product in product_description:
        p_content = product.find_next('p')
        p_text = p_content.get_text()

        # Stores product description in data dictionary
        data_dict['Product description'] = p_text

    # Finds the image content section
    image_content = soup.find('div', class_='item active')

    # Complete image URL
    if image_content:
        img_tag = image_content.find('img')
        if img_tag:
            src_image = img_tag['src']
            clean_image = src_image.removeprefix('../../../../')
            base_url_image = 'http://books.toscrape.com/'
            url_image = f'{base_url_image}{clean_image}'

            # Stores image URL in data dictionary
            data_dict['Image url'] = url_image

    # Store the product page URL in the data dictionary
    data_dict['Product page url'] = test_link

    # Append the dictionary to the list
    all_data_dicts.append(data_dict)

# Loop through all book data to count books and images
for book_data in all_data_dicts:
    product_page_url = book_data.get('Product page url')
    book_title = book_data.get('Book title')
    download_book_image(book_data)

# list of dictionaries into a DataFrame with column order
df = pd.DataFrame(all_data_dicts, columns=[
    'Book title',
    'Category',
    'Universal product code(upc)',
    'Quantity available',
    'Review rating',
    'Price excluding tax',
    'Price including tax',
    'Product description',
    'Product page url',
    'Image url'
])

# Sort columns by 'Category'
sorted_df = df.sort_values(by='Category')

# Get unique values in the sorted column
unique_categories = sorted_df['Category'].unique()

# Create separate CSV files for each category
for category in unique_categories:
    filtered_df = sorted_df[sorted_df['Category'] == category]
    filename = f'{category}_sorted_data.csv'
    filtered_df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f'Saved {filename}')

print('Process complete.')
