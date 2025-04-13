from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Optional
from . import logger
from datetime import datetime

import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
client_util = WebClient(token=os.getenv("SLACK_TOKEN"))


def get_channel_id(channel_name):
    try:
        response = client_util.conversations_list()

        for channel in response['channels']:
            if channel['name'] == channel_name:
                return channel['id']

        return f"Channel '{channel_name}' not found."

    except SlackApiError as e:
        return f"Error fetching channels: {e.response['error']}"


def get_user_info_by_user_id(client: WebClient, user_id: str) -> Optional[dict]:
    """Returns profile information for an specific user"""
    email = ""
    fullname = None
    display_name = None
    try:
        user_profile = client.users_profile_get(user=user_id)
        user_profile = user_profile.data["profile"]
    
        fullname = user_profile["real_name"]
        display_name = user_profile["display_name"]

        if "email" in user_profile:
                email = user_profile["email"]
    
    except SlackApiError as ex:
        logger.error(f"Error getting user profile: {ex}")
        if ex.response["error"] != "ratelimited":
            return None
    except Exception as ex:
        logger().warning(f"Error getting user info from slack by id: {ex}", extra={"tags": {"Consumer": "get_user_info_by_user_id"}})
        return None

    return dict(
        fullname=fullname,
        display_name=display_name,
        email=email,
    )

def validate_date_format(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def validate_dates(start_date, end_date):
    if end_date < start_date:
        return "End date cannot be earlier than start date."
    return None

def validate_top_n(top_n):
    try:
        return int(top_n)
    except (TypeError, ValueError):
        return 10  # Default value if conversion fails