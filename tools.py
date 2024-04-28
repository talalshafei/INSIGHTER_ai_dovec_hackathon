import smtplib
import pandas as pd
from email.mime.text import MIMEText
from pydantic import BaseModel, Field
from email.mime.multipart import MIMEMultipart
from web_scraping.dovec_scraping import scrape_dovec_website
from web_scraping.dogakent_scraping import scrape_dogakent_website
from web_scraping.RealEstateAnalysisTool import RealEstateAnalysisTool


class NoParamsSchema(BaseModel):
    pass


class FilePathSchema(BaseModel):
    filePath: str = Field(..., title="Filepath", description="File path required")


class SendEmailSchema(BaseModel):
    emails: str = Field(..., title="Emails", description="Emails required")
    customized_responses: str = Field(..., title="Customized Responses", description="Customized Responses required")


def find_best_property():
    """
    Finds the best property based on the customer's preferences and budget constraints.

    Returns:
        list: A list containing up to 5 best property options scraped from the Dovec website.

    Raises:
        Exception: If an error occurs during data scraping.
    """

    # max 5 because more will take so much time
    try:
        return scrape_dovec_website()[:5]
    except Exception as e:
        return str(e)


def market_analysis():
    """
    Analyzes real estate market data for Dovec and Dogakent locations, 
    providing insights into the average price per square meter, 
    property type distribution, and average price per property type.

    Returns:
        dict: A dictionary containing analysis results for Dovec and Dogakent locations.
            - For each location, the following information is provided:
                - "average_price_per_square_meter": The average price per square meter.
                - "property_type_distribution": Distribution of property types.
                - "average_price_per_property_type": Average price per property type.

    Raises:
        Exception: If an error occurs during data scraping or analysis.
    """

    try:
        # analyzing Dovec market
        dovec_data = scrape_dovec_website()
        dovec_analysis_tool = RealEstateAnalysisTool(dovec_data)
        dovec_average_price_per_square_meter = dovec_analysis_tool.average_price_per_square_meter()
        dovec_property_type = dovec_analysis_tool.property_type_distribution()
        dovec_average_price_per_property_type = dovec_analysis_tool.average_price_per_property_type()

        # analyzing Dogakent market
        dogakent_data = scrape_dogakent_website()
        dogakent_analysis_tool = RealEstateAnalysisTool(dogakent_data)
        dogakent_average_price_per_square_meter = dogakent_analysis_tool.average_price_per_square_meter()
        dogakent_property_type = dogakent_analysis_tool.property_type_distribution()
        dogakent_average_price_per_property_type = dogakent_analysis_tool.average_price_per_property_type()

        return {
            "Dovec": {
                "dovec_average_price_per_square_meter": dovec_average_price_per_square_meter,
                "dovec_property_type_distribution": dovec_property_type,
                "dovec_average_price_per_property_type": dovec_average_price_per_property_type,
            },
            "Dogakent": {
                "dogakent_average_price_per_square_meter": dogakent_average_price_per_square_meter,
                "dogakent_property_type_distribution": dogakent_property_type,
                "dogakent_average_price_per_property_type": dogakent_average_price_per_property_type,
            }
        }

    except Exception as e:
        return str(e)


def analyze_complaints():
    """
    Analyzes the complaints data to identify key trends, patterns, and insights, providing feedback to the company.

    Reads complaints data from an Excel file and performs analysis to generate two sets of information:
        1. Details of individual complaints.
        2. Counts of complaints grouped by property ID.

    Returns:
        dict: A dictionary containing two keys:
            - "complaints": JSON representation of individual complaints.
            - "complaint_counts": JSON representation of complaint counts grouped by property ID.

    Raises:
        Exception: If any other error occurs during data reading or analysis.
    """

    # get data from our server
    df = pd.read_excel('data/complaints.xlsx')
    # perform analysis
    complaint_counts = df.groupby('prop_id')['complaints'].count().reset_index()

    complaint_counts.rename(columns={'complaint': 'complaint_count'}, inplace=True)

    return {
        "complaints": df.to_json(orient='records'),
        "complaint_counts": complaint_counts.to_json(orient='records')
    }


def email_customers(emails: str, customized_responses: str):
    """
    Sends personalized email responses to customers based on the provided parameters.

    Args:
        emails (str): A string containing email addresses separated by '---'.
        customized_responses (str): A string containing customized responses separated by '---'.

    Returns:
        str: A message indicating the success of the email sending process.

    Raises:
        Exception: If an error occurs during the email sending process.
    """

    try:
        # emails and customized_responses must be converted to lists
        emails_list = emails.split("---")
        responses_list = customized_responses.split("---")

        # Email configuration
        port = 587
        sender_email = "noorulzayn10@gmail.com"
        sender_password = "bxui jote surb gxde"  # dummy password no need for .env
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
    except Exception as e:
        return str(e)

    return "Success"


def custom_json_schema(model):
    """
    Generate a custom JSON schema for the given Pydantic model, 
    so CMND.AI pass them as parameters to the intended functions.
    """

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
        "description": "Generate a comprehensive report on the current real estate market trends and developments, comparing the Dovec and Dogakent locations. Utilize the data returned to provide insights and visualize the findings. The analysis should include information such as the average price per square meter, distribution of property types, and average price per property type for both locations.",
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
        "description": "Send personalized email responses to customers who have submitted complaints. the function must take parameters: emails and customized responses both of which must be a long string separated by '---'. The function should send an email to each customer with their respective customized response. Also at the end of the email write from Dovec Customer Support , then return 'Success' if the emails are sent successfully.",
        "parameters": custom_json_schema(SendEmailSchema),
        "runCmd": email_customers,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
]
