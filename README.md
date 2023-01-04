# Rustici

This repository contains the files required to build the CSL implementation of Rustici Engine.

## Requirements

### Software

- Azure CLI
- Docker
- Python3 (further Python requirements available in `requirements.txt`)
- Azure storage explorer

### Other

- Hosts found in the `nginx/required_hosts` file should be added to your hosts file.

## Usage

### Download files

#### Requirements

- Python requirements found in `requirements.txt` (can be installed with `python -m pip install -r requirements.txt`)
- Environment variable `SUBSCRIPTION_NAME` must be set to the storage account's subscription name.

#### Detail

The Dockerfile for Rustici engine depends on two files:

- Rustici WAR zip
- MySQL connector zip

These files are stored within Azure blob storage. The `build_files.py` script is used to download them to the `resources` directory.

### Docker

#### Build

To build the docker image, use a standard `docker build` command.

#### Docker-compose

A `docker-compose.yml` file has been provided to build the entire project (with dependencies) via docker-compose; this will also build the MySQL/NGINX/Azurite images locally.

Volumes/networking are used to stitch up the services within the Docker network, which is then placed behind and NGINX reverse proxy.

## Rustici engine application

Assuming Docker compose is being used to run the project, Rustici engine will be available on the `csl.local/rustici/RusticiEngine` endpoint. This can be tested by going to `csl.local/rustici/RusticiEngine` in the browser.

### Config

The configuration for Rustici Engine (`RusticiEngineSettings.properties`) can be edited on the local client and synced into the container via volumes. To sync changes, simply restart the container.

Rustici uses environment variables in conjunction with the properties file to load configuration. These variables can be found in `./env/rusticiLocalEnv`. Changes to these values will require docker compose to be re-upped.

## NGINX

NGINX is used here as a reverse proxy, to allow Rustici and the Azurite services to run on the same domain. This is **required** by Rustici in order to prevent CORS issues when launching courses (only applicable when using the manifest import method, which CSL is. See: https://rustici-docs.s3.amazonaws.com/engine/21.1.x/Configuration/Content-Cloud.html).

Rustici will be made accessible on the `csl.local/rustici` domain.

### Config

NGINX configuration can be found in `./nginx/nginx.conf`. As with the Rustici Engine service, the configuration is synced via volumes. **Editing this configuration file is not recommended**, this allows the reverse proxy to work and by extension Rustici functionality. Any changes could negatively impact Rustci running on your local machine - NGINX problems are also notoriously hard to debug within a Docker environment.

## Azurite

Azurite is used as a local CDN/Blob storage endpoint. It allows Rustici to upload courses via manifest import, which it can then use to launch the course within the learner's browser window.

By default, Azurite is available on the `csl.local/azurite` domain. Alternatively, `localhost:9100` can be used (for connection string purposes).

### Running

The container `setup-azurite` is used to create the necessary storage container for Rustici (default: `rustici`). This container can be deleted and re-created using the Storage Explorer and re-upping.

### Connecting

To connect to Azurite, first spin up the container using Docker compose - after this open Azure Storage Explorer and create a new connectiong under 'Local and Attached' using the connection string: `DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:9100/devstoreaccount1;Q` (from https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azurite?tabs=visual-studio#http-connection-strings)

## csl-service

**The current CSL service application is a PLACEHOLDER intended to receive POST requests from Rustici's rollUp data. The entry in the docker compose file should be replaced with the Azure image of CSL-Service when it is ready for development**

CSL-Service is the business-logic layer within CSL. The existing Python app is intended to allow Rustici to post RollUp data from course engagement. The Python application will then print out some key details from the RollUp data for debugging purposes. The app itself is bound to the container via a volume, so can be edited on the host machine and redeployed if needs be. RollUp POST requests are stored in `req.json` in the root of the Dockerfile.

## Functionality

### Uploading courses

This repository makes use of an Azurite Docker image to simulate a blob storage container locally. Unzipped SCORM files should be uploaded to this container before being uploaded to Rustici (via manifest import).

**For simplicity, the name of the course (folder) should be in snake_case format**

The easiest way to do this is by using Azure Storage Explorer (https://azure.microsoft.com/en-us/products/storage/storage-explorer/); connect to the container locally and simply drag and drop the SCORM file into the `devstoreaccount1` account, under the `rustici` blob.

After this, use the `POST {{rustici_url}}/api/v2/courses?courseId={{courseID}}` endpoint (found in Postman collection) to upload the course to Rustici. The courseID should match the name of the uploaded course.

### Launching courses

### Tracking courses

## Debugging

Tomcat logs can be found in `/usr/local/tomcat/logs`. 

Rustici logs can be found using the `cat /usr/local/tomcat/logs/rusticiengine.log` command inside the container.

Rustici settings can be found using the `cat /usr/local/tomcat/lib/RusticiEngineSettings.properties` command inside the container.

NGINX access logs can be found using `cat /var/log/nginx/access.log` command inside the container.