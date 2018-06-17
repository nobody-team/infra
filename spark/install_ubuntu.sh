#!/usr/bin/env bash

cd /opt
sudo wget -O spark-2.3.1-bin-hadoop2.7.tgz http://www-eu.apache.org/dist/spark/spark-2.3.1/spark-2.3.1-bin-hadoop2.7.tgz
sudo tar xvf spark-2.3.1-bin-hadoop2.7.tgz
sudo mv spark-2.3.1-bin-hadoop2.7/ spark/
sudo rm spark-2.3.1-bin-hadoop2.7.tgz
