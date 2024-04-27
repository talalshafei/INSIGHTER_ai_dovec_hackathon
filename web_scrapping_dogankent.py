import requests
from bs4 import BeautifulSoup
import re
import csv

def scrape_dogankent_website(url, csv_filename):

    # sends the url and headers as request
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    # checks if the status code is 200 
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all elements with class "div-block-101"
        properties = soup.find_all(class_="div-block-101")
        
        # Create a list to store scraped data
        scraped_data = []
        
        # Iterate over each property
        for prop in properties:

            # Extract location information
            element = prop.find("div", class_="text-block-43")  # Find the element with class 'text-block-43'
            
            if element:
                location = element.get_text()
            else:
                # If 'text-block-43' class is not found, try finding the element with class 'text-block-41'
                element = prop.find("div", class_="text-block-41")
                if element:
                    location = element.get_text()
                else:
                    location = "Location not found"
            
            # get the price element class
            price_element = prop.find(class_="text-block-44")

            if price_element:
                #  if the price element is present, get the text of the price element
                price_text = price_element.get_text()
                
                # Use regex to extract only the digits and commas
                price_digits = re.sub(r'[^\d,]', '', price_text)
                
                # Remove commas and convert the string to an integer
                price = int(price_digits.replace(',', ''))
            else:
                price = None
            
            # Extracting square meter information from details
            details_div = prop.find(class_="div-block-102")
            details_text = ', '.join([detail.get_text().strip() for detail in details_div.find_all(class_="text-block-42")])
            square_meter = re.search(r'(\d+)(?:m²)', details_text)

            # Extracting property type information from details
            property_type_match = re.search(r'(\d+\+\d+)', details_text)
            property_type = property_type_match.group() if property_type_match else None


            if square_meter:
                square_meter = square_meter.group(1)
            else:
                square_meter = None

            # Store the data in a dictionary
            property_data = {
                "Location": location,
                "Price": price,
                "Squre-meter": square_meter,
                "property_type": property_type
            }
            
            # Append the dictionary to the list
            scraped_data.append(property_data)
        
        # Save the data to a CSV file
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Location', 'Price', 'Squre-meter', 'property_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for data in scraped_data:
                writer.writerow(data)
        
        print(f"Data saved to {csv_filename}")
    
    else:
        print("Failed to retrieve data from the website. Status code:", response.status_code)
        return None




scraped_dogankent_data = scrape_dogankent_website("https://www.101evler.com/agency-detail/dogankent-construction-estate-ltd/303", "dogankent-data.csv")

print(scraped_dogankent_data)



