import os
from dotenv import load_dotenv

load_dotenv()

def get_required_env_var(key: str):
	try:
		SUBSCRIPTION_ID=os.environ[key]
	except KeyError as e:
		raise Exception(f"{key} is a required environment variable but was not found.")

SUBSCRIPTION_ID=get_required_env_var('SUBSCRIPTION_ID')

RESOURCES_DIR=f"{os.path.dirname(__file__)}/resources"
TEMPLATES_DIR=f"{os.path.dirname(__file__)}/templates"