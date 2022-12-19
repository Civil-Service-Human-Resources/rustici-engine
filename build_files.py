import os
from azure.storage.blob import BlobServiceClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.subscription import SubscriptionClient
import zipfile
import shutil

from azure_credential import get_credential
from config import RESOURCES_DIR, SUBSCRIPTION_ID, SUBSCRIPTION_NAME

class File:
	def __init__(self, zip_name, resources_dir, blob_container) -> None:
		self.zip_name = zip_name
		self.resources_dir = resources_dir
		self.blob_container = blob_container


RUSTICI_VERSION="RusticiEngine_java_engine_21.1.19.412"
MYSQL_CONNECTOR_VERSION="mysql-connector-j-8.0.31"

STORAGE_ACCOUNT_RESOURCE_GROUP="rg-csl-utility"
RUSTICI_SA_ACCOUNT_NAME="sacslstorage"

BLOB_URL=f"https://{RUSTICI_SA_ACCOUNT_NAME}.blob.core.windows.net"

RUSTICI_FILE=File(f"{RUSTICI_VERSION}.zip", f"{RESOURCES_DIR}/rustici", "rustici/war")
MYSQL_CONNECTOR_FILE=File(f"{MYSQL_CONNECTOR_VERSION}.zip", f"{RESOURCES_DIR}/mysql", "rustici/mysql-connector")

FILES = [
	RUSTICI_FILE,
	MYSQL_CONNECTOR_FILE
]


def get_sub_id(credential, sub_name):
	sub_client = SubscriptionClient(credential=credential)
	matching_subs = [sub.subscription_id for sub in sub_client.subscriptions.list() if sub.display_name == sub_name]
	if not matching_subs:
		raise Exception(f"No matching subscriptions found with name {sub_name}")
	return matching_subs[0]


def get_blob_client():
	credential = get_credential()
	subscription_id = get_sub_id(credential, SUBSCRIPTION_NAME)
	storage_client = StorageManagementClient(credential, subscription_id=subscription_id)
	keys = storage_client.storage_accounts.list_keys(STORAGE_ACCOUNT_RESOURCE_GROUP, RUSTICI_SA_ACCOUNT_NAME)
	keys = {v.key_name: v.value for v in keys.keys}
	main_key = keys['key1']
	return BlobServiceClient(account_url=BLOB_URL, credential=main_key)


def download_and_unzip(file: File):
	blob_client = get_blob_client()
	if not os.path.exists(f"{RESOURCES_DIR}/{file.zip_name}"):
		print(f"Downloading {file.zip_name}")
		container_client = blob_client.get_container_client(container=file.blob_container)
		zip_dest_file=f"{RESOURCES_DIR}/{file.zip_name}"
		with open(zip_dest_file, "wb") as downloaded_file:
			print(f"Saving zip to {zip_dest_file}")
			blob_content = container_client.download_blob(file.zip_name).readall()
			downloaded_file.write(blob_content)
	else:
		print(f"{file.zip_name} already exists, skipping")
	
	if os.path.exists(file.resources_dir):
		print(f"Removing {file.resources_dir} directory")
		shutil.rmtree(file.resources_dir)
	
	with zipfile.ZipFile(f"{RESOURCES_DIR}/{file.zip_name}", "r") as zip_file:
		zip_file.extractall(f"{file.resources_dir}")


def copy_mysql_connector_jar():
	mysql_jar = f"{MYSQL_CONNECTOR_FILE.resources_dir}/{MYSQL_CONNECTOR_VERSION}/{MYSQL_CONNECTOR_VERSION}.jar"
	rustici_installer_lib = f"{RUSTICI_FILE.resources_dir}/RusticiEngine/Installer/lib"
	print(f"Copying \n\t{mysql_jar} \nto \n\t{rustici_installer_lib}")
	shutil.copy2(mysql_jar, rustici_installer_lib)


def run():
	print("Downloading necessary files")
	for file in FILES:
		download_and_unzip(file)
	copy_mysql_connector_jar()

	print("Done!")

run()