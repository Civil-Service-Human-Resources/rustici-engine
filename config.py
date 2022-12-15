import os
from dotenv import load_dotenv

from keyvault_client import KeyVaultConfigOption
load_dotenv()

ENVIRONMENT=os.environ.get('ENVIRONMENT', 'LOCAL')
SUBSCRIPTION_ID=os.environ['SUBSCRIPTION_ID']

RESOURCES_DIR=f"{os.path.dirname(__file__)}/resources"
TEMPLATES_DIR=f"{os.path.dirname(__file__)}/templates"

KV_ENV_MAP = {
	"LOCAL": None,
	"INTEGRATION": "kv-int",
	"STAGING": "kv-int",
	"PERFORMANCE": "kv-performance",
	"PRODUCTION": "kv-prod"
}


class RusticiXMLConfigOption(KeyVaultConfigOption):
	def __init__(self, xml_key_name, vault_key, default_value) -> None:
		super().__init__(vault_key, default_value)
		self.xml_key_name = xml_key_name


RUSTICI_CONFIG_VARS=[
	RusticiXMLConfigOption("DatabaseConnectionString", "rustici-database-connection-string", "jdbc:mysql://mysql:3306/RusticiEngineDB?user=root&password=my-secret-pw|com.mysql.cj.jdbc.Driver"),
	RusticiXMLConfigOption("ApiBasicAccounts", "rustici-api-basic-accounts", "apiuser : password"),
	RusticiXMLConfigOption("RusticiEngineUrl", "rustici-engine-url", "http://localhost:3000/RusticiEngine"),
	RusticiXMLConfigOption("RedirectOnExitUrl", "rustici-redirecton-exit-url", "http://localhost:3001")
]
