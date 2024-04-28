import requests
import xml.etree.ElementTree as ET
import requests
import re
from data.remote_urls import DOVEC_DATA


def scrape_dovec_website():

    xml_url = DOVEC_DATA

    # Send the request to the XML URL
    try:
        response = requests.get(xml_url)
    except Exception as e:
        print("Failed to send fetch data from dovec to the website.")
        raise f"Dovec Website is not reachable. {e}"

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML content
        root = ET.fromstring(response.content)

        # Create a list to store scraped data
        scraped_data = []

        # Iterate over each item tag in the XML
        for item in root.findall('item'):
            price = item.find('price').text
            if price is None or price == "0":
                # skip if price is 0
                continue

            title = item.find('title').text
            location = item.find('location').text
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
                "name": title,
                "location": location,
                "price": price,
                "currency": "pounds",
                "square_meter": square_meter,
                "property_type": property_type,
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
