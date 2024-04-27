import requests
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import re


def scrape_dovec_website():

    xml_url = "https://dovecconstruction.com/emlak.xml"

    # Send the request to the XML URL
    response = requests.get(xml_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML content
        root = ET.fromstring(response.content)

        # Create a list to store scraped data
        scraped_data = []

        # Iterate over each item tag in the XML
        for item in root.findall('item'):
            title = item.find('title').text
            location = item.find('location').text
            price = item.find('price').text
            currency = item.find('pricetype').text
            image = item.find('thumb').text
            map_location = item.find('map').text
            details = item.find('content').text.strip()

            square_meter = item.find('features/item[name="Closed Area"]/statu').text

            # Extract property type from the title
            property_type_match = re.search(r'(\d+\+\d+)', title)
            property_type = property_type_match.group() if property_type_match else "1+0"

            # Extract interior details
            interior_items = [i.text for i in item.findall('interior/item')]

            # Extract exterior details
            exterior_items = [i.text for i in item.findall('external/item')]

            # Store the data in a dictionary
            property_data = {
                "Location": location,
                "Price": price,
                "currency": currency,
                "Square Meter": square_meter,
                "Property Type": property_type,
                "property_details": details,
                "image": image,
                "map": map_location,
                "interior": interior_items,
                "exterior": exterior_items
            }

            # Append the dictionary to the list
            scraped_data.append(property_data)

        return scraped_data
    else:
        print("Failed to retrieve data from the website. Status code:", response.status_code)
        return None


# scraped_data = scrape_dovec_website()
# print(scraped_data)
