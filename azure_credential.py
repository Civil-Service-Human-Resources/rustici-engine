from azure.identity import DefaultAzureCredential

def get_credential():
	try:
		return DefaultAzureCredential()
	except Exception as e:
		raise Exception(f"Could not get Azure credentials ({e}). Are you logged into the CLI? If not are the correct environment variables set?")
