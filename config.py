import os
from dotenv import load_dotenv

load_dotenv()

SUBSCRIPTION_ID=os.environ['SUBSCRIPTION_ID']

RESOURCES_DIR=f"{os.path.dirname(__file__)}/resources"
TEMPLATES_DIR=f"{os.path.dirname(__file__)}/templates"