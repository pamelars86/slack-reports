from flask import Flask
from celery import Celery
import os
from dotenv import load_dotenv
import logging
import pyfiglet
from colorama import init, Fore
from flasgger import Swagger


load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=os.getenv("result_backend"),
        broker=os.getenv("CELERY_BROKER_URL")
    )
    celery.conf.update(app.config)
    celery.conf.broker_connection_retry_on_startup = True

    return celery

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,  # all of your endpoints
            "model_filter": lambda tag: True,  # all of your models
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)

app.config.from_mapping(
    CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL"),
    result_backend=os.getenv("result_backend"),
)
celery = make_celery(app)


init(autoreset=True)

def show_banner():
    text = "Slack Reports"
    ascii_art = pyfiglet.figlet_format(text)
    print(Fore.CYAN + ascii_art)  

show_banner()


from . import routes
