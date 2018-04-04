FROM ubuntu
ARG hub_url
ARG target_browsers=CHROME,FIREFOX,INTERNETEXPLORER

LABEL apps="Python2.7, Selenium"
LABEL maintainer="nobodyhub@gmail.com"

#
# create workdir
#
RUN mkdir /workspace
RUN chmod a+rwx /workspace
WORKDIR /workspace
RUN echo "export PATH=\$PATH:$(pwd)" >> ~/.bashrc
RUN pwd

RUN apt-get update && apt-get upgrade -y

#
# install basics
#
RUN apt-get install -y \
                    iputils-ping \
                    software-properties-common \
                    python-software-properties \
                    curl \
                    debconf-utils \
                    unzip \
                    vim \
                    wget \
                    openssh-server
#
# install applications
# 
RUN apt-get install -y \
                    python2.7 \
                    python-pip \
                    xvfb

#                   
# python components
#
RUN alias python=python2.7
RUN python --version
RUN pip install --upgrade pip
RUN pip install selenium
RUN pip install pyvirtualdisplay
RUN pip install xvfbwrapper
RUN pip install jproperties

#
# prepare the contents
# 
ADD ./ ./
RUN find . -type f
RUN chmod a+x ./entry-shell.sh
RUN pwd
RUN echo $PATH
# ENTRYPOINT ["/workspace/entry-shell.sh", "$hub_url", "$target_browsers"]
