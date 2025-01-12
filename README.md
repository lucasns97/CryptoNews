# Crypto News Alert Lambda

This project deploys an AWS Lambda function that fetches and analyzes cryptocurrency news using NewsAPI and OpenAI's GPT model. If the sentiment analysis indicates a potential market drop, an alert email is sent using Amazon SES.

## Project Structure

```
.env
.gitignore
app.py
README.md
requirements.txt
template.yml
```

## How It Works

1. **Fetch Crypto News**: The Lambda function fetches the latest news articles about a specified cryptocurrency using NewsAPI.
2. **Analyze News**: The news articles are analyzed using OpenAI's GPT model to determine the market sentiment.
3. **Send Alert**: If the analysis indicates a potential market drop, an alert email is sent using Amazon SES.

## Prerequisites

- AWS Account
- AWS CLI configured with appropriate permissions
- SAM CLI installed
- NewsAPI key
- OpenAI API key
- Amazon SES verified email

## Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a [.env](http://_vscodecontentref_/6) file** with the following content:
    ```env
    NEWS_API_KEY=your_newsapi_key
    OPENAI_API_KEY=your_openai_api_key
    ALERT_EMAIL=your_alert_email
    CRYPTO_NAME=bitcoin
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Deployment

1. **Build the SAM application**:
    ```sh
    sam build
    ```

2. **Deploy the SAM application**:
    ```sh
    sam deploy --guided
    ```

    Follow the prompts and provide the necessary parameters:
    - `NewsApiKeyParam`: Your NewsAPI key
    - `OpenAiApiKeyParam`: Your OpenAI API key
    - `AlertEmailParam`: Your email address to receive alerts
    - `CryptoNameParam`: Name of the cryptocurrency to monitor (default: Bitcoin)

## Usage

The Lambda function is triggered once a day (adjustable in [template.yml](http://_vscodecontentref_/7)). It fetches the latest news, analyzes the sentiment, and sends an alert email if a market drop is detected.

## Files

- **app.py**: Main application code.
- **template.yml**: SAM template for deploying the Lambda function.
- **requirements.txt**: Python dependencies.
- **data/**: Directory to store fetched news articles.

## License

This project is licensed under the MIT License.