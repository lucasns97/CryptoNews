from utils import CONFIG
from services.news import fetch_articles
from rich import print
from datetime import datetime

print(fetch_articles("bitcoin", date=datetime.now()))