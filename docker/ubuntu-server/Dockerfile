FROM ubuntu

LABEL apps="GIT, MAVEN, ORACLE-JDK8"
LABEL maintainer="nobodyhub@gmail.com"

RUN apt-get update && apt-get upgrade -y

#
# install basics
#
RUN apt-get install -y \
                    iputils-ping \
                    software-properties-common \
                    python-software-properties \
                    curl \
                    debconf-utils
#
# install applications
# 
RUN apt-get install -y \
                    git \
                    maven
                    

RUN apt-get purge -y openjdk-\*
RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get update
RUN echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections
RUN apt-get install -y oracle-java8-installer