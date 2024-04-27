from pydantic import BaseModel, Field
from web_scaping_dovec_2 import scrape_dovec_website
from web_scrapping_dogankent import scrape_dogankent_website
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
############# Dummy Tools ##############################
load_dotenv()

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

def email_customer(emails: list[str], customized_responses: list[str]):
    # Email configuration
    sender_email = os.getenv('EMAIL')
    sender_password = os.getenv('PASSWORD')
    server = smtplib.SMTP("smtp.gmail.com", 587)
    port = 587

    server.starttls()

    server.login(sender_email, sender_password)

    # Check if the number of emails matches the number of customized responses
    if len(emails) != len(customized_responses):
        raise ValueError("Number of emails and customized responses must match")

    # Loop through each email and customized response
    for email, customized_response in zip(emails, customized_responses):
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = 'Regarding Your High-Priority Complaint'

        # Attach customized response as message body
        body = customized_response
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP(server, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())


def market_analysis():
    dovec_data = scrape_dovec_website()[:5]
    other_data = scrape_dogankent_website()[:5]

    dovecDataFrame = pd.DataFrame(dovec_data)
    dovec_data = dovecDataFrame.to_json(orient='records')
    otherDataFrame = pd.DataFrame(other_data)
    other_data = otherDataFrame.to_json(orient='records')

    return {"dovec_data": dovec_data, "other_data": other_data}


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
        "description": "Given the customer's preferences and budget constraints, analyze the provided prompt and utilize the data returned from the function to recommend the most suitable property. Consider factors such as location, amenities, size, and any specific requirements outlined by the customer to ensure a tailored recommendation that aligns with their needs and desires and show property image if possible and location on map too.",
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
    },
    {
        "name": "market_analysis",
        "description": " Present a brief summary of the current real estate market trends and developments. Location Analysis: Visualize the average price per square meter for each location using a heatmap or bar chart. Analyze the distribution of property types in each location with a stacked bar chart or pie chart. Property Type Distribution: Display the distribution of property types using a pie chart or horizontal bar chart. Price Analysis: Compare the average price per square meter across different property types using a line graph or box plot. Conclusion: Summarize key insights and provide recommendations for stakeholders based on the analysis.",
        "parameters": custom_json_schema(NoParamsSchema),
        "runCmd": market_analysis,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }
]
