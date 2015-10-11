#!/usr/bin/env python3

__author__ = 'Tran Huu Cuong'

import time
import logging
import sys
import os
import signal

from docker import Client
from influxdb.influxdb08 import InfluxDBClient

logger = logging.getLogger('docker_mapping_mesos')
logging.basicConfig(stream=sys.stderr, level=getattr(logging, 'INFO'))


def get_list_dockerid_mapping_mesosid():
    c = Client(base_url='unix://var/run/docker.sock')

    containers = c.containers()

    list_dockerid_mapping_mesosid = list()

    for container in containers:
        if container['Names'][0].startswith('/mesos-'):
            dockerid_mapping_mesosid = list()
            dockerid_mapping_mesosid.append(container['Names'][0][1:])

            container_env = c.inspect_container(container['Id'])['Config']['Env']

            for env in container_env:
                if env.startswith('MESOS_TASK_ID'):
                    dockerid_mapping_mesosid.append(env.split('=')[1])
                    break

            if len(dockerid_mapping_mesosid) == 2:
                list_dockerid_mapping_mesosid.append(dockerid_mapping_mesosid)

    return list_dockerid_mapping_mesosid


def get_influxdb_env():
    """Get influxdb environment"""
    influxdb_env = dict()
    influxdb_env['host'] = os.environ.get('INFLUXDB_HOST', 'localhost')
    influxdb_env['port'] = os.environ.get('INFLUXDB_PORT', 8086)
    influxdb_env['username'] = os.environ.get('INFLUXDB_USER', 'root')
    influxdb_env['password'] = os.environ.get('INFLUXDB_PASS', 'root')
    influxdb_env['database'] = os.environ.get('INFLUXDB_NAME', 'cadvisor')

    return influxdb_env


def insert_list_dockerid_mapping_mesosid(list_dockerid_mapping_mesosid, influxdb_env):
    client = InfluxDBClient(
        host=influxdb_env['host'],
        port=influxdb_env['port'],
        username=influxdb_env['username'],
        password=influxdb_env['password'],
        database=influxdb_env['database']
    )

    data = dict()
    data['name'] = 'mapping'
    data['columns'] = ['container_name', 'mesos_task_id']
    data['points'] = [t for t in list_dockerid_mapping_mesosid]

    client.write_points([data])


def handler(signum=None, frame=None):
    logger.info('Signal handler called with signal {}'.format(signum))
    logger.info('Stop docker_mapping_service')
    # check if process is done
    # time.sleep(1)
    # logger.info('Wait done')
    sys.exit()


def main():
    time_interval = int(os.environ.get('TIME_INTERVAL', 10))
    influxdb_env = get_influxdb_env()

    for sign in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
        signal.signal(sign, handler)

    while True:
        try:
            list_dockerid_mapping_mesosid = get_list_dockerid_mapping_mesosid()
            insert_list_dockerid_mapping_mesosid(list_dockerid_mapping_mesosid, influxdb_env)
            logger.info('Update dockerId mapping mesosId')
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(time_interval)


if __name__ == '__main__':
    main()
