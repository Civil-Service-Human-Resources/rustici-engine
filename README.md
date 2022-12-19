# Rustici

This repository contains the files required to build the CSL implementation of Rustici Engine.

## Requirements

- Azure CLI
- Docker
- Python3 (further Python requirements available in `requirements.txt`)

## Usage

### Download files

The Dockerfile for Rustici engine depends on two files:

- Rustici WAR zip
- MySQL connector zip

These files are stored within Azure blob storage. The `build_files.py` script is used to download them to the `resources` directory.

### Build Rustici installation script

The versions of the files can be changed with the `vars.sh` file.

### Docker build

To build the docker image, use a standard `docker build` command.

A `docker-compose.yml` file has been provided to build the project via docker-compose; this will also build the MySQL image locally.

## Rustici engine application

Once the Docker container has been built and run, Rustici Engine will be available on the port provided to it. For example, using the `docker-compose.yml` will map Rustici engine to port 3000. Rustici engine will then be available on the `/RusticiEngine` endpoint. This can be tested by going to `/RusticiEngine/defaultui/admin` in the browser.

### Uploading courses

This repository makes use of an Azurite Docker image to simulate a blob storage container locally. Unzipped SCORM files should be uploaded to this container before being uploaded to Rustici (via manifest import). The easiest way to do this is by using Azure Storage Explorer (https://azure.microsoft.com/en-us/products/storage/storage-explorer/); connect to the container locally and simply drag and drop the SCORM file into the `devstoreaccount1` account, under the `test` blob.

## Debugging

Tomcat logs can be found in `/usr/local/tomcat/logs`. 

Rustici logs can be found using the `cat /usr/local/tomcat/logs/rusticiengine.log` command inside the container.

Rustici settings can be found using the `cat /usr/local/tomcat/lib/RusticiEngineSettings.properties` command inside the container.