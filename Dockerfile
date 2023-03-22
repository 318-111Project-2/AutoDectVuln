FROM ubuntu:20.04

MAINTAINER maselab318

LABEL description='AutoVulDetect (on Ubuntu)'

RUN apt-get update && \
    apt-get install -y python3  \
                       python3-pip \
                       curl \
                       make
WORKDIR /home/

COPY . /home/

CMD ["/home/install.sh"]
