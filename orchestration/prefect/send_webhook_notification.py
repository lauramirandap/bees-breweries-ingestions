import requests
from prefect import task
from jobs.utils import logger

@task
def send_webhook_notification(message: str):
    webhook_url = "https://hooks.zapier.com/hooks/catch/22387441/20uwxkm/"
    payload = {"message": message}

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        logger.info("✅ Notification sent successfully!")
    else:
        logger.info(f"❌ Failed to send notification: {response.status_code} - {response.text}")
