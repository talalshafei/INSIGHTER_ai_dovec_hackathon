from web_scaping_dovec_2 import scrape_dovec_website

class RealEstateAnalysisTool:
    def __init__(self, property_data):
        self.property_data = property_data

    def average_price_per_square_meter(self):
        # Create dictionaries to store total price and total area for each location
        total_price_per_location = {}
        total_area_per_location = {}
        properties_count_per_location = {}

        # Iterate over the property data
        for property_info in self.property_data:
            location = property_info.get("Location")  # Get location or None if missing
            price = property_info.get("Price")
            square_meter = property_info.get("Square Meter")

            # Skip if location, price, or square_meter is missing
            if location is None or price is None or square_meter is None:
                continue

            price = int(price)
            square_meter = int(square_meter)

            # Update total price, total area, and property count for the location
            total_price_per_location[location] = total_price_per_location.get(location, 0) + price
            total_area_per_location[location] = total_area_per_location.get(location, 0) + square_meter
            properties_count_per_location[location] = properties_count_per_location.get(location, 0) + 1

        # Calculate average price per square meter for each location
        average_price_per_location = {}
        for location in total_price_per_location:
            total_price = total_price_per_location[location]
            total_area = total_area_per_location[location]
            properties_count = properties_count_per_location[location]

            # Avoid division by zero and handle missing location
            if total_area != 0 and properties_count != 0:
                average_price_per_location[location] = total_price / total_area
            else:
                average_price_per_location[location] = None

        return average_price_per_location
    
    def property_type_distribution(self):
        property_type_counts = {}

        for property_info in self.property_data:
            property_type = property_info["Property Type"]
            if property_type in property_type_counts:
                property_type_counts[property_type] += 1
            else:
                property_type_counts[property_type] = 1
        
        return property_type_counts

    

scraped_data = scrape_dovec_website()

# Use the RealEstateAnalysisTool with the scraped data if scraped_data is not NULL
if scraped_data:
    # Initialize the RealEstateAnalysisTool with the scraped data
    analysis_tool = RealEstateAnalysisTool(scraped_data)

    # Example usage
    average_price = analysis_tool.average_price_per_square_meter()
    print("Average price per square meter:", average_price)

    property_type_counts = analysis_tool.property_type_distribution()
    print("Property type distribution:", property_type_counts)