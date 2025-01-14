
"""
news.py

This module provides functionality to fetch news articles using the News API.
"""

import requests
from src.utils.config import CONFIG
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List
from typing import Optional

###########
# Classes #
###########

@dataclass
class Article:
    """Data class to represent an article."""
    title: str
    description: str
    content: str
    publishedAt: str
    url: Optional[str] = None
    source: Optional[dict] = None
    author: Optional[str] = None
    urlToImage: Optional[str] = None

###########
# Methods #
###########

def fetch_articles(query: str, date: datetime = None, top_k: int = 10) -> List[Article]:
    """Fetches articles about the provided query.
    
    Args:
        query (str): The query to search for.
        date (datetime): The date to filter the articles.
        top_k (int): The maximum number of articles articles to return.
    """
    params = {
        'q': query,
        'apiKey': CONFIG.get('NEWS_API_KEY'),
        'language': 'en',
        'sortBy': 'relevance',
    }
    
    # Add date filter if provided
    if date:
        params['from'] = (date - timedelta(days=1)).strftime('%Y-%m-%d')  # Get articles from the previous day
        params['to'] = date.strftime('%Y-%m-%d')  # Get articles until the provided date
    
    # Make the request to the News API
    response = requests.get(url=CONFIG.get('NEWS_API_URL'), params=params)
    response.raise_for_status()
    
    # Parse the response
    articles = response.json().get('articles', [])[:top_k]
    articles = [Article(**article) for article in articles]
    
    return articles
