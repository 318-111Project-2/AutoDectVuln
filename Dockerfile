FROM ubuntu:20.04

MAINTAINER maselab318

LABEL description='AutoVulDetect (on Ubuntu)'

RUN apt-get update && \
    apt-get install -y python3  \
                       python3-pip \
                       curl \
                       make && \
    pip install angr \
                pwntools \
                pyfiglet \
                argparse

WORKDIR /home/

COPY . /home/

CMD ["/home/install.sh"]
