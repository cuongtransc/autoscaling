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


class Scaler:
	"""Class for Scaling"""
	def __init__(self, app_name, config):
		self.logger = logging.getLogger("autoscaling")
		self.logger.setLevel(logging.DEBUG)

		self.logger.info("Init object scaler...")
		self.config = config

		self.logger.info("Connect RESTful mariadb and get policies...")
		conn = http.client.HTTPConnection(config["MARIA_RESTFUL"]['host'], config["MARIA_RESTFUL"]['port'])
		conn.request("GET", "/app/name/"+app_name)
		json_app = conn.getresponse().read().decode("utf-8")
		self.app = json.loads(json_app)
		conn.request("GET", "/app/name/"+app_name+"/policies")
		json_policies = conn.getresponse().read().decode("utf-8")
		self.app["policies"] = json.loads(json_policies)

		self.logger.info("Connect influxdb and marathon...")
		self.influx_client = InfluxDBClient(config["INFLUXDB"]["host"], config["INFLUXDB"]["port"], config["INFLUXDB"]["username"], config["INFLUXDB"]["password"], config["INFLUXDB"]["db_name"])
		self.marathon_client = MarathonClient('http://'+config["MARATHON"]['host']+':'+config["MARATHON"]['port'])
		
		self.app["instance"] = self.marathon_client.get_app(app_name).instances
		self.app["mem"] = self.marathon_client.get_app(app_name).mem
		self.app["cpus"] = self.marathon_client.get_app(app_name).cpus

		self.logger.info("Reconfig haproxy.cfg...")
		os.system("sudo ./servicerouter.py --marathon http://"+config["MARATHON"]["host"]+":"+config["MARATHON"]["port"]+" --haproxy-config /etc/haproxy/haproxy.cfg")

		

	def get_cpu_usage(self, container_name):
		"""Return cpu usage of container_name

		@param string container_name container name  
		"""
		query = "select DERIVATIVE(cpu_cumulative_usage)  as cpu_usage from stats where container_name = '"+container_name+"' and time > now()-5m group by time(10s) "
		result = self.influx_client.query(query)
		points = result[0]["points"]
		return (points[0][1]/1000000000/self.app["cpus"])*100

	def get_container_name(self, mesos_task_id):
		"""Return container name mapping with mesos_task_id in messos
		
		@param string mesos_task_id
		"""
		query = "select container_name from "+config["INFLUXDB"]["ts_mapping"]+" where time>now() - 5m and mesos_task_id = '" +mesos_task_id+"' limit 1" 
		result = self.influx_client.query(query)
		points = result[0]["points"]
		return points[0][2]

	def get_containers_name(self):
		"""Return list all containers name of application have name app_name
		
		@param string app_name name of application
		@return list all containers name of app_name
		"""
		tasks = self.marathon_client.list_tasks(self.app["name"])
		containers_name = []
		for task in tasks:
			containers_name.append(self.get_container_name(task.id))
		return containers_name

	def avg_mem_usage(self, containers_name):
		"""Return avg memmory usage of all containers in list containers_name
		
		@param list containers_name list containers name
		@return float avg mem usage
		"""
		number_container = len(containers_name)
		containers_name = ["'"+x+"'" for x in containers_name]
		containers_name = ",".join(containers_name)
		query = "select DERIVATIVE(memory_usage)  as memory_usage,container_name from stats where  time > now()-5m and  container_name in ("+containers_name+") group by time(10s),container_name limit "+str(number_container)
		result = self.influx_client.query(query)
		points = result[0]["points"]
		sum_memory_usage = 0
		for point in points:
			sum_memory_usage += points[0][1]/self.app["mem"]*100
		return sum_memory_usage / number_container

	def avg_cpu_usage(self, containers_name):
		"""Return avg cpu usage of all containers in list containers_name
		
		@param list containers_name list containers name
		@return float avg cpu usage
		"""
		number_container = len(containers_name)
		containers_name = ["'"+x+"'" for x in containers_name]
		containers_name = ",".join(containers_name)
		query = "select DERIVATIVE(cpu_cumulative_usage)  as cpu_usage,container_name from stats where  time > now()-5m and  container_name in ("+containers_name+") group by time(10s),container_name limit "+str(number_container)
		result = self.influx_client.query(query)
		points = result[0]["points"]
		#return points[0][1]/1000000000/self.app["cpus"]*100
		sum_cpu_usage = 0
		for point in points:
			sum_cpu_usage += points[0][1]/1000000000/self.app["cpus"]*100
		return sum_cpu_usage / number_container

	def scale(self, delta):
		"""sacle app_name (add or remove) delta intances
		
		@param string app_name name of application
		@param int delta number intances add or remove
		"""
		new_instance = self.app["instance"] + delta
		if(new_instance > self.app['max_instances']):
			new_instance = self.app['max_instances']
		if(new_instance < self.app['min_instances']):
			new_instance = self.app['min_instances']
		if(new_instance != self.app["instance"]):
			self.marathon_client.scale_app(self.app["name"], new_instance)
			self.logger.info("Scaling "+self.app["name"]+" to: "+str(new_instance))
			self.logger.info("Waiting for config file haproxy.cfg...")
			time.sleep(self.config["TIME"]['w_config_ha'])
			self.logger.info("Config file haproxy.cfg...")
			os.system("sudo ./servicerouter.py --marathon http://"+config["MARATHON"]["host"]+":"+config["MARATHON"]["port"]+" --haproxy-config /etc/haproxy/haproxy.cfg")
			self.app["instance"] = marathon_client.get_app(self.app["name"]).instances
			self.logger.info("Sleep "+str(self.config["TIME"]['after_scale'])+"s...")
			time.sleep(self.config["TIME"]['after_scale'])


	def check_rule(self, policie, value, type):
		"""Check rule and return number intances need scale
		
		@param models.Policie policies
		@param tuple value values of metric
		@return integer number intances need scale
		"""
		delta["up"] = 0
		delta["down"] = 0
		# Check upper_threshold
		if(value[policie["metric_type"]] > policie["upper_threshold"]):
			delta['up'] = policie["instances_in"]
		# Check lower_threshold
		if(value[policie["metric_type"]] < policie["lower_threshold"]):
			delta['down'] = policie["instances_out"]
		
		return delta


	def autoscaling(self):
		while True:
			try:
				containers_name = self.get_containers_name(self.app["name"])
				avg_cpu = self.avg_cpu_usage(containers_name)
				avg_mem = self.avg_mem_usage(containers_name)
				self.logger.info("Avg cpu usage:"+str(avg_cpu)+", avg memmory usage: "+ str(avg_mem))
				rs_detal['up'] = 0
				rs_detal['down'] = 10
				for policie in self.app["policies"]:
					delta = self.check_rule(self.policie, (cpu, mem))
					if(rs_detal['up'] < delta['up']):
						rs_detal['up'] = delta['up']
					if(rs_detal['down'] > delta['down']):
						rs_detal['down'] = delta['down']

				if(rs_detal['up'] > 0):
					self.scale(self.app["name"], rs_detal['up'])
				elif(rs_detal['down'] > 0):
					self.scale(self.app["name"], 0-rs_detal['down'])
			except Exception as e:
				self.logger.exception(e)
			finally:
				time.sleep(self.config["TIME"]['monitor'])

def main():
	scaler = Scaler(argv[1], CONFIG)
	scaler.autoscaling()
if __name__ == '__main__':
    main()




	

