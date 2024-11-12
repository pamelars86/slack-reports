import os

class Config:
    SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    result_backend = os.getenv("result_backend")