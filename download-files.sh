#!/usr/bin/env bash
source vars.sh
ACCOUNT_NAME="sacslstorage"

echo "Setting account key"
ACCOUNT_KEY=$(az storage account keys list --resource-group rg-csl-utility --account-name $ACCOUNT_NAME --query '[0].value' -o tsv)

echo "Downloading Rustici war"
az storage blob download -f "./resources/$RUSTICI_VERSION" -c rustici/war -n "$RUSTICI_VERSION" --account-name "$ACCOUNT_NAME" --account-key="$ACCOUNT_KEY"
echo "Downloading MYSQL connector"
az storage blob download -f "./resources/$MYSQL_CONNECTOR" -c rustici/mysql-connector -n "$MYSQL_CONNECTOR" --account-name "$ACCOUNT_NAME" --account-key="$ACCOUNT_KEY"