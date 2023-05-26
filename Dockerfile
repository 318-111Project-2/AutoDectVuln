FROM ubuntu:20.04
MAINTAINER maselab318

LABEL description='AutoVulDetect (on Ubuntu)' 

WORKDIR /home/
COPY . /home/

RUN apt-get update && \
    apt-get install -y python3  \
                       python3-pip \
                       curl \
                       make &&  \
    pip3 install -r requirements.txt

WORKDIR /home/lib/web/

RUN python3 app/database/init_db.py
# RUN python3 web.py
CMD ["python3","web.py"]