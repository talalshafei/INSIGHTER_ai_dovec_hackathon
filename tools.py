from pydantic import BaseModel, Field
import pandas as pd
# from web_scraping_dovec import scrape_dovec_website_save
from web_scaping_dovec_2 import scrape_dovec_website

############# Dummy Tools ##############################


class NoParamsSchema(BaseModel):
    pass


class FilePathSchema(BaseModel):
    filePath: str = Field(..., title="Filepath", description="File path required")

def file_reader(filePath: str):
    try:
        with open(filePath, 'r') as file:
            return file.read()
    except Exception as e:
        return str(e)


def find_best_property():
    dovec_scraped_data = scrape_dovec_website()[:5]
    return dovec_scraped_data


def suggest_response_customer():
    file = pd.read_excel('sample_customer_data.xlsx')
    # get response from our server
    return file
    


def classify_response(response: str):
    pass


# def market_analysis():
#     dovec_data = scrape_dovec_website()
#     # other_data = scrape_other_website()
#     return {"dovec_data": dovec_data, "other_data": other_data}


def custom_json_schema(model):
    schema = model.schema()
    properties_formatted = {
        k: {
            "title": v.get("title"),
            "type": v.get("type")
        } for k, v in schema["properties"].items()
    }

    return {
        "type": "object",
        "default": {},
        "properties": properties_formatted,
        "required": schema.get("required", [])
    }


tools = [
    {
        "name": "find_best_property",
        "description": "Given the customer's preferences and budget constraints, analyze the provided prompt and utilize the data returned from the function to recommend the most suitable property. Consider factors such as location, amenities, size, and any specific requirements outlined by the customer to ensure a tailored recommendation that aligns with their needs and desires and show its image if possible and the map too.",
        "parameters": custom_json_schema(NoParamsSchema),
        "runCmd": find_best_property,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },

    {
        "name": "suggest_response_customer",
        "description": "Suggest a response to all the customers based on their previous responses that you read from the file data",
        "parameters": custom_json_schema(NoParamsSchema),
        "runCmd": suggest_response_customer,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }

    # {
    #     "name": "market_analysis",
    #     "description": "Conduct a thorough analysis of prevailing market trends within the real estate sector, leveraging data sourced from the Dovec website as well as other reputable platforms. Evaluate key metrics including average property prices, demand-supply dynamics, regional variations, and pertinent market indicators. Provide nuanced insights into market conditions, highlighting emerging patterns, potential investment opportunities, and any significant factors shaping the current landscape. Your analysis should offer a comprehensive overview, empowering stakeholders with actionable intelligence to make informed decisions within the dynamic real estate market",
    #     "parameters": custom_json_schema(NoParamsSchema),
    #     "runCmd": market_analysis,
    #     "isDangerous": False,
    #     "functionType": "backend",
    #     "isLongRunningTool": False,
    #     "rerun": True,
    #     "rerunWithDifferentParameters": True
    # }

]
