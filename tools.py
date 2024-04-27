from pydantic import BaseModel, Field
from web_scaping_dovec_2 import scrape_dovec_website
from web_scrapping_dogankent import scrape_dogankent_website
from RealEstateAnalysisTool import RealEstateAnalysisTool
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

############# Dummy Tools ##############################


class NoParamsSchema(BaseModel):
    pass


class FilePathSchema(BaseModel):
    filePath: str = Field(..., title="Filepath", description="File path required")


class SendEmail(BaseModel):
    email: list[str] = Field(..., title="Email", description="Email address required")
    customized_response: list[str] = Field(..., title="Email", description="Response required")


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
    return file.to_json()


def email_customer(email: str, customized_response: str):
    # Email configuration
    sender_email = 'your_email@example.com'
    sender_password = 'your_email_password'
    smtp_server = 'smtp.example.com'
    smtp_port = 587

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = 'Regarding Your High-Priority Complaint'

    body = customized_response
    # Attach message body
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())


def market_analysis():
    dovec_data = scrape_dovec_website()
    dovecDataFrame = pd.DataFrame(dovec_data)
    dovec_data_json = dovecDataFrame.to_json(orient='records')
    dovec_analysis_tool = RealEstateAnalysisTool(dovec_data)
    dovec_average_price = dovec_analysis_tool.average_price_per_square_meter()
    dovec_property_type = dovec_analysis_tool.property_type_distribution()

    # other_data = scrape_dogankent_website()
    # otherDataFrame = pd.DataFrame(other_data)
    # other_data_json = otherDataFrame.to_json(orient='records')
    # other_analysis_tool = RealEstateAnalysisTool(other_data)
    # other_average_price = other_analysis_tool.average_price_per_square_meter()
    # other_property_type = other_analysis_tool.property_type_distribution()

    response = {
        "dovec": {
            # "data": dovec_data_json,
            "average_price": dovec_average_price,
            "property_type": dovec_property_type
        },
        # "other_data": {
        #     "data": other_data_json,
        #     "average_price": other_average_price,
        #     "property_type": other_property_type,
        # }
    }

    return response


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
        "name": "market_analysis",
        "description": "Conduct a thorough analysis of prevailing market trends within the real estate sector, leveraging data sourced from the Dovec website as well as other reputable platforms. Evaluate key metrics including average metric property prices, average price per square meter, regional variations, and pertinent market indicators. Provide nuanced insights into market conditions, highlighting emerging patterns, potential investment opportunities, and any significant factors shaping the current landscape. Your analysis should offer a comprehensive overview, empowering stakeholders with actionable intelligence to make informed decisions within the dynamic real estate market, be aware the data is structured in a json that has two keys one for Dovec and one for their competitors and it contains full data and other statistics",
        "parameters": custom_json_schema(NoParamsSchema),
        "runCmd": market_analysis,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": True,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }
]
