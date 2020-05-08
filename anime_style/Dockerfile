FROM ubuntu:18.04

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && apt-get install -y libsm6 libxext6 libXrender.so.1 \
    && pip3 install -r /tmp/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

ADD ./src /server

WORKDIR /server

CMD python3 /server/main.py