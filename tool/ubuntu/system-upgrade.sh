#!/usr/bin/env bash

# Update Ubuntu version to the latest release version
# User Interaction is inevitable during `do-release-upgrade`
# NOTE:
#   Possible to suffer data lost and configuration change

apt-get update
apt-get upgrade -y
apt-get dist-upgrade
apt-get install update-manager-core -y
do-release-upgrade -m server

