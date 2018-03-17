FROM ubuntu

# Need to run with `--privileged` for `docker run`

LABEL apps="Git, Maven, Python2.7, Selenium, Firefox"
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
                    git \
                    maven \
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

#
# install firefox
#
RUN apt-get install -y firefox 
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.18.0-linux64.tar.gz
RUN chmod +x geckodriver
RUN mv geckodriver /usr/bin
RUN rm geckodriver-v0.18.0-linux64.tar.gz

#
# prepare the contents
# 
ADD ./ ./
RUN find . -type f
RUN chmod a+x ./entry-shell.sh
RUN pwd
RUN echo $PATH
#ENTRYPOINT ["/workspace/entry-shell.sh"]
