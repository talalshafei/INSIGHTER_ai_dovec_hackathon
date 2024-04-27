from pydantic import BaseModel, Field
from RealEstateAnalysisTool import RealEstateAnalysisTool
from web_scaping_dovec_2 import scrape_dovec_website
from web_scrapping_dogankent import scrape_dogankent_website
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv


load_dotenv()


class NoParamsSchema(BaseModel):
    pass


class FilePathSchema(BaseModel):
    filePath: str = Field(..., title="Filepath", description="File path required")

class SendEmailSchema(BaseModel):
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
    
    port = 587
    sender_email = os.getenv('EMAIL')
    sender_password = os.getenv('PASSWORD')
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    server.login(sender_email, sender_password)

    # Check if the number of emails matches the number of customized responses
    if len(emails) != len(customized_responses):
        raise ValueError("Number of emails and customized responses must match")

    # Loop through each email and customized response
    for email, customized_response in zip(emails, customized_responses):
        # Create message
        msg = MIMEMultipart("alternative")
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = 'Regarding Your Complaint'

        # Attach customized response as message body
        body = customized_response
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server.sendmail(sender_email, email, msg.as_string())
    
    server.quit()


def market_analysis():
    dovec_data = scrape_dovec_website()[:5]
    other_data = scrape_dogankent_website()[:5]

    dovecDataFrame = pd.DataFrame(dovec_data)
    dovec_data_json = dovecDataFrame.to_json(orient='records')
    dovec_analysis_tool = RealEstateAnalysisTool(dovec_data)
    dovec_average_price = dovec_analysis_tool.average_price_per_square_meter()
    dovec_property_type = dovec_analysis_tool.property_type_distribution()

    # other_data = scrape_dogankent_website()
    # otherDataFrame = pd.DataFrame(other_data)
    # other_data_json = otherDataFrame.to_json(orient='records')
    # other_analysis_tool = RealEstateAnalysisTool(other_data)
    # other_average_price = other_analysis_tool.average_price_per_square_meter()""
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


def analyze_complaints():
    # get data from our server
    df = pd.read_excel('complaints.xlsx')
    # perform analysis
    complaint_counts = df.groupby('prop_id')['complaints'].count().reset_index()

    complaint_counts.rename(columns={'complaint': 'complaint_count'}, inplace=True)

    return {
        "complaints": df.to_json(orient='records'),
        "complaint_counts": complaint_counts.to_json(orient='records')
    }


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
    },
    {
        "name": "email_customer",
        "description": "Send customized emails to the list of customers",
        "parameters": custom_json_schema(SendEmailSchema),
        "runCmd": email_customer,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }
]
