from dotenv import load_dotenv
from os import environ

load_dotenv('config.env')

BOT_TOKEN = environ.get("TOKEN")
GENERAL_CHANNEL_ID = environ.get("GENERAL_CHANNEL_ID")
