FROM ubuntu

# Need to run with `--privileged` for `docker run`

LABEL apps="Git, Maven, Python2.7, Selenium, Google Chrome"
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
# install google driver
# google-chrome need to run in a non-super user
# please pay attention to the versio of google-chrome and chromedriver
#
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update
RUN apt-get install -y google-chrome-stable \
                       libxi6 \
                       libgconf-2-4

RUN curl -O http://chromedriver.storage.googleapis.com/2.36/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN chmod +x chromedriver
RUN mv chromedriver /usr/bin
RUN rm chromedriver_linux64.zip

#
# prepare the contents
# 
ADD ./ ./
RUN find . -type f
RUN chmod a+x ./entry-shell.sh
RUN useradd -m -p selenium -s /bin/bash selenium
USER selenium # google-chrome running as root without --no-sandbox is not supported.
RUN pwd
RUN echo $PATH
#ENTRYPOINT ["/workspace/entry-shell.sh"]
