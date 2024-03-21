#!/bin/bash

# Update your existing list of packages
sudo apt-get update

# Install a few prerequisite packages which let apt use packages over HTTPS
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add the GPG key for the official Docker repository to your system
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add the Docker repository to APT sources
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update the package database with the Docker packages from the newly added repo
sudo apt-get update

# Make sure you are about to install from the Docker repo instead of the default Ubuntu repo
sudo apt-cache policy docker-ce

# Install Docker
sudo apt-get install -y docker-ce

# Add the current user to the Docker group
sudo usermod -aG docker ${USER}

# Install Docker Compose
DOCKER_COMPOSE_VERSION=1.29.2
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

