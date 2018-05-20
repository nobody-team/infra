#!/usr/bin/env bash
#---------------------------------------------
#
# Install SonarQube on Ubuntu
#
# Packages include:
#   * SonarQube
#   * Oracle JDK8
#   * PostgreSQL
#
# Reference:
#       https://www.vultr.com/docs/how-to-install-sonarqube-on-ubuntu-16-04
#
#---------------------------------------------


#
# Perform a system update
#
sudo apt-get update
sudo apt-get -y upgrade

#
# Install JDK
#
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudosudo apt install oracle-java8-installer

#
# Install and configure PostgreSQL
#
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
sudo apt-get -y install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
# update password for postgres
sudo passwd postgres
su - postgres
createuser sonar
psql
# update password for DB user sonar
ALTER USER sonar WITH ENCRYPTED password 'sonar';
\q

#
# Download SonarQube
#
wget https://sonarsource.bintray.com/Distribution/sonarqube/sonarqube-6.4.zip
apt-get -y install unzip
sudo unzip sonarqube-6.4.zip -d /opt
sudo mv /opt/sonarqube-6.4 /opt/sonarqube

#
# Configure SonarQube
#

#sudo vi /opt/sonarqube/conf/sonar.properties
#```
#sonar.jdbc.username=sonar
#sonar.jdbc.password=sonar
#sonar.jdbc.url=jdbc:postgresql://localhost/sonar
#```

#
# Configure Systemd service
#

#vi /etc/systemd/system/sonar.service
#```
#[Unit]
#Description=SonarQube service
#After=syslog.target network.target
#
#[Service]
#Type=forking
#
#ExecStart=/opt/sonarqube/bin/linux-x86-64/sonar.sh start
#ExecStop=/opt/sonarqube/bin/linux-x86-64/sonar.sh stop
#
#User=root
#Group=root
#Restart=always
#
#[Install]
#WantedBy=multi-user.target
#```

#
# Configure Sonar Service
#

# Start the application
#sudo systemctl start sonar

# Enable the SonarQube service to automatically start at boot time.
#sudo systemctl enable sonar

# To check if the service is running
#sudo systemctl status sonar