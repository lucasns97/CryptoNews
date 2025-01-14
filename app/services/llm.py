"""
llm.py

This module provides functionality to analyze news articles using an LLM (GPT) 
to determine if a specific cryptocurrency's price is likely to drop based on the 
sentiment of the articles.
"""

import json
from openai import OpenAI
from utils import CONFIG
from services.news import Article
from typing import List

# Instantiate the OpenAI client with the provided API key from configuration
llm_client = OpenAI(api_key=CONFIG.get('OPENAI_API_KEY'))

###########
# Methods #
###########

def generate_prompt(news_articles: List[Article], crypto_name: str) -> str:
    """
    Generate a prompt for the LLM based on the provided news articles and 
    cryptocurrency name.

    Args:
        news_articles (list): A list of dictionaries, each containing 'title',
                              'description', and 'content' of a news article.
        crypto_name (str): The name of the cryptocurrency to analyze.

    Returns:
        str: A well-structured prompt to be used by the LLM.
    """
    prompt = (
        f"Act as a cryptocurrency specialist and analyze the following news "
        f"articles about {crypto_name} and determine if the market sentiment "
        "indicates a price drop.\n\n"
        "Then, answer using the exact following JSON pattern:\n\n```json\n"
        "{\"Reasoning\": \"[explanation with quotes]\", \"ValueWillDrop\": [true/false]}\n```\n\n"
        "DATA:\n\"\"\"\n"
    )

    for article in news_articles:
        prompt += (
            f"- Title: {article.title}\n"
            f"  Description: {article.description}\n"
            f"  Content: {article.content}\n\n"
        )
    prompt += "\"\"\""
    return prompt

def call_model(prompt: str, llm_client: OpenAI) -> str:
    """
    Call the LLM (OpenAI) with the given prompt to analyze its content.

    Args:
        prompt (str): The prompt to send to the LLM.
        llm_client (OpenAI): The instantiated OpenAI client.

    Returns:
        str: The raw string response from the LLM.
    """
    completion = llm_client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful cryptocurrency and market specialist assistant."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

def parse_response(response: str) -> dict:
    """
    Parse the response from the LLM into a JSON object.

    Args:
        response (str): The raw response string from the LLM.

    Returns:
        dict: A dictionary containing the parsed JSON data.
    """
    # Strip any JSON formatting artifacts like ```json and ```
    cleaned_response = response.strip("```json\n").strip("```")

    # Convert to a Python dictionary
    json_object = json.loads(cleaned_response)
    return json_object

def analyze_news_with_llm(news_articles: List[Article], crypto_name: str) -> dict:
    """
    Analyze the provided list of news articles using the LLM to determine if 
    the market sentiment indicates a price drop.

    Args:
        news_articles (list): A list of dictionaries, each containing 'title', 
                              'description', and 'content'.
        crypto_name (str): The name of the cryptocurrency to analyze.

    Returns:
        dict: A dictionary containing the LLM's reasoning and whether the value 
              will drop (True/False).
    """
    prompt = generate_prompt(news_articles, crypto_name)
    response = call_model(prompt, llm_client)
    try:
        parsed_response = parse_response(response)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse the response from the LLM. Response is invalid:\n\n" + response)
    return parsed_response
