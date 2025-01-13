import os
import json
import boto3
import requests
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
from datetime import datetime
import random
from openai import OpenAI

# Configurations
# Load environment variables from .env file if running locally
if os.getenv('AWS_EXECUTION_ENV') is None:
    load_dotenv()

NEWS_API_URL = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv('NEWS_API_KEY')  # API Key for NewsAPI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # API Key for OpenAI
CRYPTO_NAME = os.getenv('CRYPTO_NAME')  # Name of the cryptocurrency to analyze
ALERT_EMAIL = os.getenv('ALERT_EMAIL')  # Your email to receive alerts

# Initialize SES client
ses_client = boto3.client('ses', region_name='us-east-1')
llm_client = OpenAI(api_key=OPENAI_API_KEY)

def fetch_crypto_news(crypto_name):
    """Fetches news about the cryptocurrency."""
    params = {
        'q': crypto_name,
        'apiKey': NEWS_API_KEY,
        'language': 'en',
        'sortBy': 'relevance',
    }
    url = f"{NEWS_API_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get('articles', [])

def store_news_articles(news_articles, crypto_name, filename='./data/news.json'):
    """Stores the news articles to a JSON file."""
    # Get timestamp for the current time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Update filename
    filename = filename.replace('.json', f'_{crypto_name}_{timestamp}.json')

    # Check if the data folder exists
    if not os.path.exists('./data'):
        os.makedirs('./data')

    # Write the news articles to a JSON file
    with open(filename, 'w') as file:
        json.dump(news_articles, file, indent=4)

def random_select_news(news_articles, num_articles=10):
    """Randomly selects a subset of news articles."""
    return random.sample(news_articles, num_articles)

def analyze_news_with_llm(news_articles):
    """Analyzes the news with GPT to determine market trend."""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    def generate_prompt(news_articles, crypto_name):
        """Generates a prompt for the LLM based on news articles."""
        prompt = f"Act as a cryptocurrency specialist and analyze the following news articles about {crypto_name} and determine if the market sentiment indicates a price drop.\n\n"
        prompt += f"Then, answer using the exact following JSON pattern:\n\n```json\n{{\"Reasoning\": \"[explanation with quotes]\", \"ValueWillDrop\": [true/false]}}\n```\n\n"
        prompt += "DATA:\n\"\"\"\n"
        for article in news_articles:
            prompt += f"- Title: {article['title']}\n  Description: {article['description']}\n  Content: {article['content']}\n\n"
        prompt += "\"\"\""
        return prompt
    
    def call_model(prompt):
        """Calls the OpenAI API to analyze the prompt."""
        completion = llm_client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "system", "content": "You are a helpful cryptocurrency and market specialist assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return completion.choices[0].message.content

    def parse_response(response):
        """Parses the response from the LLM."""
        # Step 1: Clean the string
        cleaned_response = response.strip("```json\n").strip("```")

        # Step 2: Convert to JSON object
        json_object = json.loads(cleaned_response)
        
        return json_object

    prompt = generate_prompt(news_articles, CRYPTO_NAME)
    response = call_model(prompt)
    parsed_response = parse_response(response)
    return parsed_response

def send_email_alert(justification):
    """Sends an alert email using Amazon SES with the model's justification."""
    subject = f"Alert: Potential {CRYPTO_NAME} Market Drop Detected"
    body = (
        f"Based on the latest news, the sentiment analysis suggests a possible drop in {CRYPTO_NAME} market value.\n"
        "Consider reviewing the news and market trends immediately.\n\n"
        f"Justification:\n{justification}"
    )
    try:
        response = ses_client.send_email(
            Source=ALERT_EMAIL,
            Destination={'ToAddresses': [ALERT_EMAIL]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        return response
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Email error: {e}")
        return None

def lambda_handler(event, context):
    """Main function for AWS Lambda."""
    try:
        news_articles = fetch_crypto_news(CRYPTO_NAME)
        if not news_articles:
            print("No news articles found.")
            return {"statusCode": 200, "body": "No news articles available."}

        # Select articles
        filtered_articles = random_select_news(news_articles, 30)
        
        # Analyze news articles
        analysis = analyze_news_with_llm(filtered_articles)

        if analysis.get("ValueWillDrop", False):
            send_email_alert(analysis.get("Reasoning", "No reasoning provided."))
            return {"statusCode": 200, "body": "Alert email sent.", "analysis": analysis}
        else:
            return {"statusCode": 200, "body": "No market drop detected.", "analysis": analysis}
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": str(e)}

if __name__ == "__main__":
    print(lambda_handler(None, None))