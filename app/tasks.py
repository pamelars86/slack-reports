from . import celery
from .slack_client import fetch_messages

@celery.task
def fetch_messages_task(channel, start_date, end_date):
    messages = fetch_messages(channel, start_date, end_date)
    return messages