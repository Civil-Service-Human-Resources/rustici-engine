import os
from azure.storage.blob import BlobServiceClient
from azure.mgmt.storage import StorageManagementClient
import zipfile
import shutil

from azure_credential import get_credential
from config import RESOURCES_DIR, SUBSCRIPTION_ID, TEMPLATES_DIR
from rustici_config import generate_rustici_config

class File:
	def __init__(self, zip_name, resources_dir, blob_container) -> None:
		self.zip_name = zip_name
		self.resources_dir = resources_dir
		self.blob_container = blob_container

DB_HOST=os.environ.get('DB_HOST', 'mysql:3306')
DB_USER=os.environ.get('DB_USER', 'root')
DB_PASSWORD=os.environ.get('DB_PASSWORD', 'my-secret-pw')

RUSTICI_VERSION="RusticiEngine_java_engine_21.1.19.412"
MYSQL_CONNECTOR_VERSION="mysql-connector-j-8.0.31"

INSTALLATION_SCRIPT="installScript.sh"
INSTALLATION_SCRIPT_TEMPLATE=f"{TEMPLATES_DIR}/{INSTALLATION_SCRIPT}"
INSTALLATION_SCRIPT=f"{RESOURCES_DIR}/{INSTALLATION_SCRIPT}"

STORAGE_ACCOUNT_RESOURCE_GROUP="rg-csl-utility"
RUSTICI_SA_ACCOUNT_NAME="sacslstorage"

BLOB_URL=f"https://{RUSTICI_SA_ACCOUNT_NAME}.blob.core.windows.net"

RUSTICI_FILE=File(f"{RUSTICI_VERSION}.zip", f"{RESOURCES_DIR}/rustici", "rustici/war")
MYSQL_CONNECTOR_FILE=File(f"{MYSQL_CONNECTOR_VERSION}.zip", f"{RESOURCES_DIR}/mysql", "rustici/mysql-connector")

FILES = [
	RUSTICI_FILE,
	MYSQL_CONNECTOR_FILE
]


def get_blob_client():
	credential = get_credential()
	storage_client = StorageManagementClient(credential, subscription_id=SUBSCRIPTION_ID)
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


def build_install_script():
	print("Building Rustici install script")
	existing_content = ""
	with open(INSTALLATION_SCRIPT_TEMPLATE, "r") as file:
		existing_content = file.read()

	existing_content=existing_content.replace("DB_HOST", DB_HOST)
	existing_content=existing_content.replace("DB_USER", DB_USER)
	existing_content=existing_content.replace("DB_PASSWORD", DB_PASSWORD)

	with open(INSTALLATION_SCRIPT, "w") as file:
		file.write(existing_content)


def run():
	print("Downloading necessary files")
	for file in FILES:
		download_and_unzip(file)
	copy_mysql_connector_jar()
	build_install_script()
	print("Generating Rustici configuration")
	generate_rustici_config()

	print("Done!")

run()