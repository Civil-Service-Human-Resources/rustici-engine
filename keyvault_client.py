from azure_credential import get_credential
from config import ENVIRONMENT
from azure.keyvault.secrets import SecretClient


class KeyVaultConfigOption:
	def __init__(self, vault_key, default_value) -> None:
		self.vault_key=vault_key
		self.default_value=default_value


KV_ENV_MAP = {
	"LOCAL": None,
	"INTEGRATION": "kv-int",
	"STAGING": "kv-int",
	"PERFORMANCE": "kv-performance",
	"PRODUCTION": "kv-prod"
}


def generate_kv_url():
	print(f"Generating keyvault URL for {ENVIRONMENT} environment")
	keyvault_name = KV_ENV_MAP.get(ENVIRONMENT)
	if (keyvault_name):
		return f"https://{keyvault_name}.vault.azure.net"
	else:
		return None


def load_vars(vars: list[KeyVaultConfigOption]):
	keyvault_url = generate_kv_url()
	if keyvault_url:
		secret_client = SecretClient(vault_url=keyvault_url, credential=get_credential())
		return {key.vault_key: lambda k: secret_client.get_secret(k.vault_key) for key in vars}
	else:
		print(f"{ENVIRONMENT} doesn't have a keyvault mapped, using default/local variables")
		return {key.vault_key: key.default_value for key in vars}