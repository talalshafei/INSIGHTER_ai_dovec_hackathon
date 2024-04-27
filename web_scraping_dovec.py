import requests
from bs4 import BeautifulSoup
import re
import csv


def scrape_dovec_website_save(url, csv_filename):

    # sends the url and headers as request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    # checks if the status code is 200
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all elements with class "description"
        properties = soup.find_all(class_="description")

        # Create a list to store scraped data
        scraped_data = []

        # Iterate over each property
        for prop in properties:

            title = prop.find(class_="title").get_text()

            price = prop.find(class_="current").get_text()

            # Extracting property type information from title
            property_type_match = re.search(r'(\d+\+\d+)', title)
            property_type = property_type_match.group() if property_type_match else "1+0"

            # extract squre meter
            square_meter = prop.find('div', class_='layer-setup').find('span', class_='attr').text.strip()

            # Store the data in a dictionary
            property_data = {
                "Location": title,
                "Price": price,
                "Squre-meter": square_meter,
                "property_type": property_type
            }

            # Append the dictionary to the list
            scraped_data.append(property_data)

        # Save the data to a CSV file
        # with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        #     fieldnames = ['Location', 'Price', 'Squre-meter', 'property_type']
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #     writer.writeheader()
        #     for data in scraped_data:
        #         writer.writerow(data)

        # print(f"Data saved to {csv_filename}")

    else:
        print("Failed to retrieve data from the website. Status code:", response.status_code)
        return None

    return scraped_data


# scrape_dovec_data = scrape_dovec_website_save(
#     "https://dovecconstruction.com/en/real-estate/?filter%5Bsearch%5D=&filter%5Bcategory%5D=0&filter%5Btype%5D=0&filter%5Bcity%5D=0&filter%5Bdistrict%5D=0&filter%5Bmin%5D=10&filter%5Bmax%5D=400", "dovec-ai-data.csv")


# print(scrape_dovec_data)
