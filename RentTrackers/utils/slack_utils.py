import os
import logging
import requests

post_message_url = "https://slack.com/api/chat.postMessage"


def send_notification(city, count):
    try:
        message = f"Scraped {count} listings from {city}"
        slack_token = os.environ["SLACK_TOKEN"]
        data = {
            "channel": "craigslist",
            "text": message,
            "token": slack_token,
        }

        requests.post(post_message_url, data)
    except Exception as e:
        logging.error(e)
