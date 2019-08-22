import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(city, count):
    try:
        sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
        from_email = os.environ["FROM_EMAIL"]
        to_email = os.environ["TO_EMAIL"]

        message = Mail(
                    from_email=from_email,
                    to_emails=to_email,
                    subject='Craigslist Scraper: {0} - {1}'.format(city, count),
                    html_content='<strong>Have a good day</strong>zs'
                )
        sg.send(message)

    except Exception as e:
        logging.error(e)