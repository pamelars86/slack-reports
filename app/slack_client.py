import time
import backoff
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
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

@backoff.on_exception(
    backoff.expo,
    SlackApiError,
    max_time=300,
    jitter=backoff.full_jitter,
    giveup=lambda e: e.response["error"] != "ratelimited",
    on_backoff=lambda details: logger.info(f"Retrying... {details}")
)
def fetch_thread_by_ts(channel: str, thread_ts: str) -> dict:
    """Fetch a complete thread by thread timestamp
    
    Args:
        channel: The channel ID
        thread_ts: The thread timestamp (e.g., "1748458889.115369")
        
    Returns:
        Dictionary containing the main message and all replies
    """
    try:
        # Get the complete conversation including all replies
        response = client.conversations_replies(
            channel=channel,
            ts=thread_ts,
            inclusive=True
        )
        
        messages = response["messages"]
        if not messages:
            return {"error": "Thread not found"}
        
        # First message is the main thread message
        main_message = messages[0]
        replies = messages[1:] if len(messages) > 1 else []
        
        # Format main message
        formatted_main = {
            "author": main_message.get("user"),
            "message": main_message.get("text", ""),
            "post_id": main_message.get("ts"),
            "url": f"{slack_home}/archives/{channel}/p{main_message.get('ts', '')[:10]}.{main_message.get('ts', '')[-6:]}",
            "date": datetime.fromtimestamp(float(main_message.get("ts", 0))).isoformat(),
            "reactions": {r["name"]: r["count"] for r in main_message.get("reactions", [])},
        }
        
        # Format replies
        formatted_replies = []
        for reply in replies:
            formatted_reply = {
                "author": reply.get("user"),
                "message": reply.get("text", ""),
                "post_id": reply.get("ts"),
                "url": f"{slack_home}/archives/{channel}/p{reply.get('ts', '')[:10]}.{reply.get('ts', '')[-6:]}",
                "date": datetime.fromtimestamp(float(reply.get("ts", 0))).isoformat()
            }
            formatted_replies.append(formatted_reply)
        
        return {
            "main_message": formatted_main,
            "replies": formatted_replies,
            "total_messages": len(messages)
        }
        
    except SlackApiError as e:
        logger.error(f"Error fetching thread: {e}")
        logger.error(f"Error response: {e.response}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error fetching thread: {e}")
        return {"error": f"Unexpected error: {str(e)}"}