from utils import CONFIG
from services.news import fetch_articles
from services.llm import analyze_news_with_llm
from services.email import send_email_alert
from datetime import datetime

def lambda_handler(event: dict, context: dict) -> dict:
    """Main function for AWS Lambda."""
    try:
        # Fetch news articles
        today = datetime.now()
        news_articles = fetch_articles(CONFIG.get("CRYPTO_NAME"), date=today, top_k=10)
        if not news_articles:
            return {"statusCode": 200, "body": "No news articles available."}

        # Analyze news articles
        analysis = analyze_news_with_llm(news_articles)

        # Send email alert if a market drop is detected
        if analysis.get("ValueWillDrop", False):
            send_email_alert(analysis.get("Reasoning", "No reasoning provided."))
            return {"statusCode": 200, "body": "Alert email sent.", "analysis": analysis}
        else:
            return {"statusCode": 200, "body": "No market drop detected.", "analysis": analysis}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}

if __name__ == "__main__":
    print(lambda_handler(None, None))