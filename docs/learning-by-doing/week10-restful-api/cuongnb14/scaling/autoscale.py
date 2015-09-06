#! /usr/bin/env python3
"""Auto scaling server

author: cuongnb14@gmail.com
"""

from sys import argv
import json
from influxdb.influxdb08 import InfluxDBClient
import time
import http.client
import os
from config import *
from marathon import MarathonClient 
import sys
import logging
import models

client = InfluxDBClient(INFLUXDB["host"], INFLUXDB["port"], INFLUXDB["username"], INFLUXDB["password"], INFLUXDB["db_name"])
marathon_client = MarathonClient('http://'+MARATHON['host']+':'+MARATHON['port'])
app = None
number_instance = 0

logger = logging.getLogger("autoscaling")
logger.setLevel(logging.DEBUG)

def get_cpu_usage(container_name):
	"""Return cpu usage of container_name

	@param string container_name container name  
	"""
	query = "select DERIVATIVE(cpu_cumulative_usage)  as cpu_usage from stats where container_name = '"+container_name+"' and time > now()-5m group by time(10s) "
	result = client.query(query)
	points = result[0]["points"]
	return points[0][1]/1000000000/4*100

def get_container_name(mesos_task_id):
	"""Return container name mapping with mesos_task_id in messos
	
	@param string mesos_task_id
	"""
	query = "select container_name from "+INFLUXDB["ts_mapping"]+" where time>now() - 5m and mesos_task_id = '" +mesos_task_id+"' limit 1" 
	result = client.query(query)
	points = result[0]["points"]
	return points[0][2]

def get_containers_name(app_name):
	"""Return list all containers name of application have name app_name
	
	@param string app_name name of application
	@return list all containers name of app_name
	"""
	tasks = marathon_client.list_tasks(app_name)
	containers_name = []
	for task in tasks:
		containers_name.append(get_container_name(task.id))
	return containers_name

def avg_cpu_usage(containers_name):
	"""Return avg cpu usage of all containers in list containers_name
	
	@param list containers_name list containers name
	@return float avg cpu usage
	"""
	number_container = len(containers_name)
	containers_name = ["'"+x+"'" for x in containers_name]
	containers_name = ",".join(containers_name)
	query = "select DERIVATIVE(cpu_cumulative_usage)  as cpu_usage,container_name from stats where  time > now()-5m and  container_name in ("+containers_name+") group by time(10s),container_name limit "+str(number_container)
	result = client.query(query)
	points = result[0]["points"]
	return points[0][1]/1000000000/4*100

	sum_cpu_usage = 0
	for point in points:
		sum_cpu_usage += points[0][1]/1000000000/4*100
	return sum_cpu_usage / number_container

def scale(app_name, delta):
	"""sacle app_name (add or remove) delta intances
	
	@param string app_name name of application
	@param int delta number intances add or remove
	"""
	marathon_client.scale_app(app_name, delta=delta)
	logger.info("scaling "+app_name+": "+str(delta))
	logger.info("waiting for config file haproxy.cfg...")
	time.sleep(TIME['w_config_ha'])
	logger.info("config file haproxy.cfg")
	os.system("sudo ./servicerouter.py --marathon http://"+MARATHON["host"]+":"+MARATHON["port"]+" --haproxy-config /etc/haproxy/haproxy.cfg")

def check_rule(policie, value):
	"""Check rule and scale if true
	
	@param models.Policie policies
	@param float value value of metric type
	@return boolean, True if violation else return False
	"""
	global number_instance
	global app
	if(policie.metric_type == 0):
		if(value > policie.upper_threshold):
			if(number_instance < app.max_instances):
				scale(app.name, policie.instances_in)
				number_instance = marathon_client.get_app(app.name).instances
				logger.info("sleep "+str(TIME['in_up'])+"s...")
				time.sleep(TIME['in_up'])
			else:
				logger.info("number intances is maximum")
			return True
		elif(value < policie.lower_threshold):
			if(number_instance > app.min_instances):
				scale(app.name, 0-policie.instances_out)
				number_instance = marathon_client.get_app(app.name).instances
				logger.info('scaled up done, current number intances: '+str(number_instance))
				logger.info("sleep "+str(TIME['in_down'])+"s...")
				time.sleep(TIME['in_down'])
			else:
				logger.info("number intances is minximum")
			return True
	if(policie.metric_type == 1):
		pass
	return False


def main():
	app_name = argv[1]
	global app
	app = models.get_app_of_appname(app_name)
	global number_instance
	number_instance = marathon_client.get_app(app_name).instances
	while True:
		try:
			containers_name = get_containers_name(app_name)
			avg_cpu = avg_cpu_usage(containers_name)
			logger.info("avg cpu usage:"+str(avg_cpu))

			policies = models.get_policies_of_appname(app_name)
			for policie in policies:
				if(check_rule(policie, avg_cpu)):
					break
		except Exception as e:
			logger.exception(e)
		finally:
			time.sleep(TIME['monitor'])
if __name__ == '__main__':
    main()




	

