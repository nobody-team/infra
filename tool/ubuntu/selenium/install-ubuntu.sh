#!/usr/bin/env bash

# Run with `sudo ./install-ubuntu.sh`
# Following Components will be installed by this scripts
# * Python2.7 + Selenium#
# * xvfb
# * Chrome
# * Firefox

# Preparation
apt-get update
sudo apt-get install openssh-server -y

# Install Python + Selenium
apt-get install python2.7 -y
apt-get install python-pip -y
pip install --upgrade pip
pip install selenium

# Install xvfb
apt-get install xvfb -y
pip install pyvirtualdisplay

# Install Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install google-chrome-stable -y

curl -O http://chromedriver.storage.googleapis.com/2.24/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/bin
rm chromedriver_linux64.zip

# Install Firefox
apt-get install firefox -y

wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
tar -xvzf geckodriver-v0.18.0-linux64.tar.gz
chmod +x geckodriver
mv geckodriver /usr/bin
rm geckodriver-v0.18.0-linux64.tar.gz
