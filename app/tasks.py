from . import celery
from .slack_client import fetch_messages
from collections import defaultdict
from datetime import datetime, timedelta
from . import logger
from .utils import get_user_info_by_user_id
from slack_sdk import WebClient
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

client = WebClient(token=os.getenv("SLACK_TOKEN"))

@celery.task(bind=True)
def fetch_messages_task(self, channel_id, p_start_date, p_end_date):
    messages = []

    chunk_size = timedelta(days=7)  # Ex.: process 7 days at a time

    start_date = datetime.strptime(p_start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
    end_date = datetime.strptime(p_end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

    current_start = start_date

    while current_start < end_date:
        current_end = min(current_start + chunk_size, end_date)

        chunk_messages = fetch_messages(channel_id, int(current_start.timestamp()), int(current_end.timestamp()))

        messages.extend(chunk_messages)

        current_start = current_end

        self.update_state(state='PROGRESS', meta={'current_start': current_start.isoformat()})

    return messages

@celery.task(bind=True)
def calculate_top_repliers_task(self, channel_id, p_start_date, p_end_date, top_n=10):
    top_repliers_data = defaultdict(lambda: {"discussions": 0, "responses": 0, "full_name": ""})

    chunk_size = timedelta(days=7)  # Ex.: process 7 days at a time

    start_date = datetime.strptime(p_start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
    end_date = datetime.strptime(p_end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

    current_start = start_date

    while current_start < end_date:
        current_end = min(current_start + chunk_size, end_date)

        messages = fetch_messages(channel_id, int(current_start.timestamp()), int(current_end.timestamp()))

        for msg in messages:
            parent_author = msg['author']
            repliers_set = set()

            for reply in msg.get("replies", []):
                reply_author = reply["author"]

                if reply_author != parent_author:
                    if reply_author not in repliers_set:
                        top_repliers_data[reply_author]["discussions"] += 1
                        repliers_set.add(reply_author)
                    top_repliers_data[reply_author]["responses"] += 1

        current_start = current_end

    sorted_repliers = sorted(
        top_repliers_data.items(),
        key=lambda x: (-x[1]['discussions'], -x[1]['responses'])
    )[:top_n]

    top_repliers_ids = [author for author, _ in sorted_repliers]

    full_names = {
        user_id: get_user_info_by_user_id(client, user_id)
        for user_id in top_repliers_ids
    }

    result = [
        {
            "id_replier": author,
            "full_name_replier": full_names.get(author, "Unknown"),
            "discussions": data["discussions"],
            "responses": data["responses"]
        }
        for author, data in sorted_repliers
    ]

    return result