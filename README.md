# Rustici

This repository contains the files required to build the CSL implementation of Rustici Engine.

## Requirements

- Azure CLI
- Docker

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

## Debugging

Tomcat logs can be found in `/usr/local/tomcat/logs`. 