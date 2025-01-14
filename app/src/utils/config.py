import os
from dotenv import load_dotenv

# Global configuration
CONFIG = {}

def load_config():
    """Loads the configuration from the environment variables."""
    global CONFIG
    
    # Load environment variables from .env file if running locally
    if os.getenv('AWS_EXECUTION_ENV') is None:
        load_dotenv()
    
    CONFIG = {
        'NEWS_API_URL': "https://newsapi.org/v2/everything",
        'NEWS_API_KEY': os.getenv('NEWS_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'CRYPTO_NAME': os.getenv('CRYPTO_NAME'),
        'ALERT_EMAIL': os.getenv('ALERT_EMAIL'),
    }

# Load the configuration
load_config()
