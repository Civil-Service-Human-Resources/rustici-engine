from config import RESOURCES_DIR, RUSTICI_CONFIG_VARS, TEMPLATES_DIR
import xml.etree.ElementTree as ET

from keyvault_client import load_vars

RUSTICI_PROPERTIES_FILE="RusticiEngineSettings.properties"
RUSTICI_CONFIG_TEMPLATE=f"{TEMPLATES_DIR}/{RUSTICI_PROPERTIES_FILE}"
RUSTICI_CONFIG=f"{RESOURCES_DIR}/{RUSTICI_PROPERTIES_FILE}"
RUSTICI_CONFIG_XML_HEADER="""
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
"""


def generate_rustici_config_xml(var_map: dict):
	tree = ET.parse(RUSTICI_CONFIG_TEMPLATE)
	properties_root = tree.getroot()
	for k, v in var_map.items():
		elem = ET.SubElement(properties_root, 'entry')
		elem.set("key", k)
		elem.text = v
	ET.indent(tree)
	with open(RUSTICI_CONFIG, "wb") as f:
		f.write(RUSTICI_CONFIG_XML_HEADER.strip().encode("utf8"))
		tree.write(f, "utf-8")


def generate_rustici_config():
	vars = load_vars(RUSTICI_CONFIG_VARS)
	var_map = {var.xml_key_name : vars[var.vault_key] for var in RUSTICI_CONFIG_VARS}
	generate_rustici_config_xml(var_map)