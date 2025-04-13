import time
import backoff
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.llm_client import generate_summary_with_llm
from .utils import get_user_info_by_user_id

from . import logger
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

client = WebClient(token=os.getenv("SLACK_TOKEN"))
slack_home = os.getenv("SLACK_HOME")

if not client:
    logger.error("SLACK_API_TOKEN debe estar configurado en el entorno")

    raise EnvironmentError("SLACK_API_TOKEN deve estar configurado no ambiente")
else:
    logger.info("Cliente de Slack creado con éxito")

@backoff.on_exception(
    backoff.expo,                   # Exponential backoff strategy
    SlackApiError,                  # Exception to catch
    max_time=300,                   # Max time to retry in seconds (5 minutes)
    jitter=backoff.full_jitter,     # Add jitter to avoid spikes
    giveup=lambda e: e.response["error"] != "ratelimited",  # only retry if it's ratelimited
    on_backoff=lambda details: logger.info(f"Retrying... {details}")
)
def fetch_messages(channel, start_date, end_date):
    messages = []
    try:
        start_ts = start_date
        end_ts = end_date
        next_cursor = None

        while True:
            try:
                response = client.conversations_history(
                    channel=channel,
                    oldest=start_ts,
                    latest=end_ts,
                    limit=100,
                    cursor=next_cursor
                )
                for msg in response['messages']:
                    post_id =  msg.get("ts")
                    user_id = msg.get("user")
                    # user_info = get_user_info_by_user_id(client, user_id)
                    
                    formatted_msg = {
                        "author": user_id,
                       # "fullname": user_info["email"],
                        "message": msg.get("text"),
                        "post_id": post_id,
                        "url": f"{slack_home}/archives/{channel}/p{post_id[:10]}.{post_id[-6:]}",
                        "date": datetime.fromtimestamp(float(msg.get("ts"))).isoformat(),
                        "reactions": {r["name"]: r["count"] for r in msg.get("reactions", [])},
                        "replies": [],
                        "subtype": msg.get("subtype")
                    }

                    if "reply_count" in msg:
                        replies_response = fetch_replies(channel, msg["ts"])
                        formatted_msg["replies"] = replies_response

                        # TODO Generate summary for the entire thread (message + replies)
                        thread_content = msg["text"] + " ".join(reply["message"] for reply in replies_response)
                        # formatted_msg["summary"] = generate_summary_with_llm(thread_content)
                    #else:
                        # TODO Generate summary only for the message without replies
                        # formatted_msg["summary"] = generate_summary_with_llm(msg["text"])


                    messages.append(formatted_msg)

                next_cursor = response.get("response_metadata", {}).get("next_cursor")
                if not next_cursor:
                    break

            except SlackApiError as e:
                logger.error(f"Error paginating messages: {e}")
                logger.error(f"Error response in paginating messages: {e.response}")
                return {"error": str(e)}

    except SlackApiError as e:
        logger.error(f"Error fetching messages: {e}")
        logger.error(f"Error response in fetching messages: {e.response}")
        return {"error": str(e)}

    return messages

@backoff.on_exception(
    backoff.expo,                   # Exponential backoff strategy
    SlackApiError,                  # Exception to catch
    max_time=300,                   # Max time to retry in seconds (5 minutes)
    jitter=backoff.full_jitter,     # Add jitter to avoid spikes
    giveup=lambda e: e.response["error"] != "ratelimited",  # only retry if it's ratelimited
    on_backoff=lambda details: logger.info(f"Retrying... {details}")
)
def fetch_replies(channel, ts):
    try:
        replies_response = client.conversations_replies(
            channel=channel,
            ts=ts
        )
        return [
            {
                "author": reply.get("user"),
                "message": reply.get("text"),
                "post_id": reply.get("ts"),
                "url": f"{slack_home}/archives/{channel}/p{reply.get('ts')[:10]}.{reply.get('ts')[-6:]}",
                "date": datetime.fromtimestamp(float(reply.get("ts"))).isoformat()
            } for reply in replies_response["messages"] if reply.get("ts") != ts
        ]
    except SlackApiError as e:
        logger.error(f"Error fetching replies: {e}")
        logger.error(f"Error response in fetching replies: {e.response}")

        if 'error' in e.response and e.response["error"] == "ratelimited":
            logger.info("Rate limit error detected. Applying backoff.")
        raise e

def fetch_top_repliers():
    return []