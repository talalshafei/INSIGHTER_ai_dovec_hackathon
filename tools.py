from pydantic import BaseModel, Field
from RealEstateAnalysisTool import RealEstateAnalysisTool
from web_scaping_dovec import scrape_dovec_website
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class NoParamsSchema(BaseModel):
    pass


class FilePathSchema(BaseModel):
    filePath: str = Field(..., title="Filepath", description="File path required")


class SendEmailSchema(BaseModel):
    emails: str = Field(..., title="Emails", description="Emails required")
    customized_responses: str = Field(..., title="Customized Responses", description="Customized Responses required")

def filter_property_data(prompt, data):
    keywords = prompt.lower().split()
    filtered_properties = []
    for property in data:
        if all(keyword in property['Location'].lower() or
               keyword in property['property_details'].lower() or
               keyword in property['Property Type'].lower() for keyword in keywords):
            filtered_properties.append({
                "Name": property["Name"],
                "Location": property["Location"],
                "Price": property["Price"],
                "currency": property["currency"],
                "Square Meter": property["Square Meter"],
                "Property Type": property["Property Type"],
                "image": property["image"]
            })
    return filtered_properties

def find_best_property(prompt):
    #dovec_scraped_data = scrape_dovec_website()
    #return dovec_scraped_data
    dovec_scraped_data = scrape_dovec_website()
    filtered_properties = filter_property_data(prompt, dovec_scraped_data)
    
    return filtered_properties


def email_customers(emails: str, customized_responses: str):
    # emails and customized_responses must be converted to lists
    emails_list = emails.split("---")
    responses_list = customized_responses.split("---")

    # Email configuration
    port = 587
    sender_email = "noorulzayn10@gmail.com"
    sender_password = "bxui jote surb gxde"
    server = smtplib.SMTP("smtp.gmail.com", port)
    server.ehlo()
    server.starttls()

    server.login(sender_email, sender_password)

    # Loop through each email and customized response
    for email, response in zip(emails_list, responses_list):
        # Create message
        msg = MIMEMultipart("alternative")
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Apology and Resolution: Addressing Your Recent Concerns"

    # Attach customized response as message body
        body = response
        msg.attach(MIMEText(body, 'plain'))

    # Send email
        server.sendmail(sender_email, email, msg.as_string())

    server.quit()

    return "Success"


def market_analysis():
    dovec_data = scrape_dovec_website()
    dovec_analysis_tool = RealEstateAnalysisTool(dovec_data)
    dovec_average_price_per_square_meter = dovec_analysis_tool.average_price_per_square_meter()
    dovec_property_type = dovec_analysis_tool.property_type_distribution()
    dovec_average_price_per_property_type = dovec_analysis_tool.average_price_per_property_type()

    return {
        "average_price_per_square_meter": dovec_average_price_per_square_meter,
        "property_type_distribution": dovec_property_type,
        "average_price_per_property_type": dovec_average_price_per_property_type,
    }


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
        "name": "market_analysis",
        "description": "Present a brief summary of the current real estate market trends and developments. Location Analysis: Visualize the average price per square meter for each location using a heatmap or bar chart. Analyze the distribution of property types in each location with a stacked bar chart or pie chart. Property Type Distribution: Display the distribution of property types using a pie chart or horizontal bar chart. Price Analysis: Compare the average price per square meter across different property types using a line graph or box plot. Conclusion: Summarize key insights and provide recommendations for stakeholders based on the analysis.",
        "parameters": custom_json_schema(NoParamsSchema),
        "runCmd": market_analysis,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": True,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "analyze_complaints",
        "description": "Analyze the complaints data to identify key trends, patterns, and insights. Present the findings in a clear and compelling manner, enabling stakeholders to gain a deeper understanding of the underlying issues and rank them based on importance. Your analysis should highlight common themes, recurring problems, and potential areas for improvement, providing valuable insights to inform decision-making and drive positive change. Also make customized responses for solution and apology for each complaint.",
        "parameters": custom_json_schema(NoParamsSchema),
        "runCmd": analyze_complaints,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "email_customers",
        "description": "Send personalized email responses to customers who have submitted complaints. the function must take parameters: emails and customized responses both of which must be a long string separated by '---'. The function should send an email to each customer with their respective customized response. then return 'Success' if the emails are sent successfully.",
        "parameters": custom_json_schema(SendEmailSchema),
        "runCmd": email_customers,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
]
