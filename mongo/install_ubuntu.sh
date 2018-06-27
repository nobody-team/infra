#!/usr/bin/env bash

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4

# 14.04
#echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

# 16.04
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list

sudo apt-get update
sudo apt-get install -y mongodb-org

# Install the latest version of MongoDB
sudo apt-get install -y mongodb-org

# Install a specific release of MongoDB
#sudo apt-get install -y mongodb-org=4.0.0 mongodb-org-server=4.0.0 mongodb-org-shell=4.0.0 mongodb-org-mongos=4.0.0 mongodb-org-tools=4.0.0

# Start/Stop/Restart MongoDB
#sudo service mongod start
#sudo service mongod stop
#sudo service mongod restart

# Uninstall MongoDB
#sudo service mongod stop
#sudo apt-get purge mongodb-org*
#sudo rm -r /var/log/mongodb
#sudo rm -r /var/lib/mongodb
