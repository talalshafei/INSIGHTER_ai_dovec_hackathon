import os
from pydantic import BaseModel, Field
import requests

############# Dummy Tools ##############################


class ProductFinderSchema(BaseModel):
    product: str = Field(..., title="Product", description="Product name required")


# class WeatherCitySchema(BaseModel):
#     city: str = Field(..., title="City", description="City name required")


def product_finder(product: str):
    url = f"https://dummyjson.com/products/search?q={product}"
    response = requests.get(url)
    return response.json()


# def weather_from_location(city: str):
#     api_key = os.getenv('WEATHER_API_KEY')
#     if not api_key:
#         raise ValueError("API key for weather data is not set in environment variables.")
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
#     response = requests.get(url)
#     return response.json()


######### END ###########################################################################################

class FilePathSchema(BaseModel):
    filePath: str = Field(..., title="Filepath", description="File path required")


class RoleBasedReportPathSchema(BaseModel):
    reportPath: str = Field(..., title="ReportPath", description="Report path required")
    role: str = Field(..., title="Role", description="Role required")


def file_reader(filePath: str):
    try:
        with open(filePath, 'r') as file:
            return file.read()
    except Exception as e:
        return str(e)


def summarize_report_based_on_role(reportPath: str, role: str):
    try:
        with open(reportPath, 'r') as reportFile:
            return {"role": role, "report": reportFile.read()}
    except Exception as e:
        return str(e)


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
        "name": "summarize_report",
        "description": "Generate a comprehensive summary, no longer than 4000 words, from a lengthy report file. Ensure the summary effectively captures the key findings, insights, recommendations, and all sections present in the report",
        "parameters": custom_json_schema(FilePathSchema),
        "runCmd": file_reader,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": True,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "summarize_report_based_on_role",
        "description": "Generate a concise summary, up to 4000 words, from a lengthy report file tailored to the specified role. Ensure the summary is highly relevant to the role, comprehensible to the user and contain all sections present in the report, leveraging their background for better understanding.",
        "parameters": custom_json_schema(RoleBasedReportPathSchema),
        "runCmd": summarize_report_based_on_role,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": True,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "customer_summary_report",
        "description": "Create a compelling summary, limited to 1000 words, from a lengthy report file. Ensure the summary effectively communicates key findings, insights, and recommendations to engage potential customers and foster positive sentiment towards the company",
        "parameters": custom_json_schema(FilePathSchema),
        "runCmd": file_reader,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": True,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    # {
    #     "name": "weather_from_location",
    #     "description": "Gets the weather details from a given city name",
    #     "parameters": custom_json_schema(WeatherCitySchema),
    #     "runCmd": weather_from_location,
    #     "isDangerous": False,
    #     "functionType": "backend",
    #     "isLongRunningTool": False,
    #     "rerun": True,
    #     "rerunWithDifferentParameters": True
    # },
    {
        "name": "file_reader",
        "description": "Returns the contents of a file given its filepath",
        "parameters": custom_json_schema(FilePathSchema),
        "runCmd": file_reader,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "product_finder",
        "description": "Finds and returns dummy products details based on the product name passed to it",
        "parameters": custom_json_schema(ProductFinderSchema),
        "runCmd": product_finder,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }
]
