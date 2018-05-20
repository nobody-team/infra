#!/usr/bin/env bash

#---------------------------------------------
#
# Install Jenkins on Ubuntu
#
# Packages include:
#   * Jenkins
#   * OpenSSH(optional)
#
# Reference:
#       https://www.digitalocean.com/community/tutorials/how-to-install-jenkins-on-ubuntu-16-04
#
#---------------------------------------------

wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | sudo apt-key add -
echo deb https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list
sudo apt-get update
sudo apt-get install jenkins -y

#
# Configure Jenkins server
#

# Start server
#sudo systemctl start jenkins

# Check server status
#sudo systemctl status jenkins

# Firewall settings(optional)
#sudo ufw allow 8080
#sudo ufw status
#sudo ufw allow OpenSSH
#sudo ufw enable

#
# Initial password
#
#sudo cat /var/lib/jenkins/secrets/initialAdminPassword

#
# Server configuration
#

# Change default port(8080)
#sudo vi /etc/default/jenkins