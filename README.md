# Scraping Book Data from [http://books.toscrape.com/]

This program is designed to scrape book data from the website [http://books.toscrape.com/]. It extracts information such as book titles, categories, ratings, prices, and images. The scraped data is then organized and stored in a CSV file for each category.

## Prerequisites

### Virtual Environment
Create a virtual environment to manage your project dependencies. You can create a virtual environment using `python -m venv venv` and activate it before installing dependencies.

Activate the virtual environment before running the installation commands.

Make sure you have the following Python libraries installed:

- requests
- BeautifulSoup
- time
- os
- pandas

You can install them using:

```bash
# In your command line or terminal
pip install requests beautifulsoup4 pandas

## Running the Program

To run the program, execute the following command:

```bash
python webscrape.py

Modifying Running Times

You can modify the running times by adjusting the following constants in the code:

    MAX_RETRIES: Maximum number of retries for page responses.
    TIMEOUT_SECONDS: Total timeout for the program.
    PAGE_RESPONSE_TIMEOUT: Timeout for individual page responses.
    timeout_seconds: Timeout for the scraping process. (Specify time in seconds with no delimiter, including spaces)

Output

The program outputs a CSV file for each category with the scraped book data. The files are named [category]_sorted_data.csv. Images of the books are downloaded to the 'images' folder.
Important Notes

The program requires good and constant internet access to scrape data from the http://books.toscrape.com/ website.

GitHub Repository

https://github.com/gonzalezedgarphone/BooksOnline.git

Feel free to adjust according to your preferences.