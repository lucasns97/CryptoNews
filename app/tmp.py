from datetime import datetime, timedelta
from src.services.news import fetch_articles
from rich import print
from lambda_function import lambda_handler

if __name__ == '__main__':
    # articles = fetch_articles('bitcoin', date=datetime.now())
    # for article in articles:
    #     article.update_content()
    # print(articles)
    print(lambda_handler(None, None))