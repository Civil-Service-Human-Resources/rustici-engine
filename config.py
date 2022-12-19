import os
from dotenv import load_dotenv

load_dotenv()

def get_required_env_var(key: str):
	try:
		return os.environ[key]
	except KeyError as e:
		raise Exception(f"{key} is a required environment variable but was not found.")

SUBSCRIPTION_NAME=get_required_env_var('SUBSCRIPTION_NAME')

RESOURCES_DIR=f"{os.path.dirname(__file__)}/resources"
TEMPLATES_DIR=f"{os.path.dirname(__file__)}/templates"