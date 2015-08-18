# Author: Tran Huu Cuong
# Date: 2015-07-22

FROM ubuntu:14.04
MAINTAINER Tran Huu Cuong "tranhuucuong91@gmail.com"

# using apt-cacher-ng proxy for caching deb package
#RUN echo 'Acquire::http::Proxy "http://172.17.42.1:3142/";' >> /etc/apt/apt.conf.d/01proxy

RUN apt-get update -qq \
    && apt-get install -y python3 python3-pip build-essential python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY app/docker_mapping_mesos.py /app/docker_mapping_mesos.py
RUN chmod +x /app/docker_mapping_mesos.py

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

WORKDIR /app
CMD ["docker_mapping_mesos.py"]
