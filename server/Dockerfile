FROM ubuntu:18.04

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update \
    && apt-get install -y gcc libpq-dev vim curl git unzip \
    && apt-get install -y python3.7 python3-pip python3.7-dev \
    && ln -sf /usr/bin/python3.7 /usr/bin/python3 \
    && apt-get install -y libsm6 libxext6 libxrender-dev \
    && pip3 install -r /tmp/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && apt-get autoremove -y gcc git

ADD ./src/magic_style /web

WORKDIR /web

RUN ln -sfv /web/magic_style/settings.py.pro /web/magic_style/settings.py

CMD bash /web/run.sh