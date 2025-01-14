"""
email.py

This module provides functionality to send an email alert using Amazon SES.
"""

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from utils import CONFIG

# Initialize SES client
ses_client = boto3.client('ses', region_name='us-east-1')

###########
# Methods #
###########

def send_email_alert(justification: str, crypto_name: str) -> dict:
    """Sends an alert email using Amazon SES with the model's justification."""
    subject = f"Alert: Potential {crypto_name} Market Drop Detected"
    body = (
        f"Based on the latest news, the sentiment analysis suggests a possible drop in {crypto_name} market value.\n"
        "Consider reviewing the news and market trends immediately.\n\n"
        f"Justification:\n{justification}"
    )
    try:
        response = ses_client.send_email(
            Source=CONFIG.get('ALERT_EMAIL'),
            Destination={'ToAddresses': [CONFIG.get('ALERT_EMAIL')]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        return response
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Email error: {e}")
        return None
