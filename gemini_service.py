import os

from dotenv import load_dotenv
from google import genai


# Load .env file
load_dotenv()


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")


# Create Gemini client
client = genai.Client(api_key=api_key)


def generate_response(message, customer, article):

    prompt = f"""
You are a customer support assistant.

Customer message:
{message}

Customer information:
Name: {customer["name"]}
Plan: {customer["plan"]}
Service: {customer["service"]}
Billing: {customer["billing_status"]}
Account: {customer["account_status"]}

Knowledge Base Article:
Title: {article["title"]}
Content: {article["content"]}

Task:
Understand the customer's problem and provide a short,
professional support response.

Use only the information provided above.
Do not invent information.
If the information is not enough, ask for the required information.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text