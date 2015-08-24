#! /usr/bin/env python3
# author: cuongnb14@gmail.com



from sys import argv
import json
from influxdb.influxdb08 import InfluxDBClient
import time
import http.client
import os


host = "localhost"
port = 8086
user = 'root'
password = 'root'
dbname = 'cadvisor'
dbname_mapping = 'mapping'

client = InfluxDBClient(host, port, user, password, dbname)

def getCPUUsage(container_name):
	query = "select DERIVATIVE(cpu_cumulative_usage)  as cpu_usage from stats where container_name = '"+container_name+"' and time > now()-5m group by time(10s) "
	result = client.query(query)
	points = result[0]["points"]
	return points[0][1]/1000000000/4*100

def getContainerName(mesos_task_id):
	query = "select container_name from mapping where time>now() - 5m and mesos_task_id = '" +mesos_task_id+"' limit 1" 
	result = client.query(query)
	points = result[0]["points"]
	return points[0][2]

def getContainersName(app_name):
	query = "select DISTINCT(mesos_task_id) from mapping where time > now() - 5m"
	result = client.query(query)
	points = result[0]["points"]
	containers_name = []
	for point in points:
		mesos_task_id = point[1]
		if (mesos_task_id.find(app_name, 0) > -1):
			containers_name.append(getContainerName(point[1]))
	return containers_name

def avgCPUUsage(containers_name):
	sum_cpu_usage = 0
	for container_name in containers_name:
		sum_cpu_usage += getCPUUsage(container_name)
	return sum_cpu_usage / len(containers_name)

def scale(app_name, number):
	HOST_NAME = 'localhost:8080'
	HEADER = {'Content-type': 'application/json'}
	data = '{"instances": '+ str(number) +'}'
	url = '/v2/apps/' + app_name
	connect = http.client.HTTPConnection(HOST_NAME)
	connect.request('PUT',url,data,HEADER)
	print('config: config file haproxy.cfg')
	os.system("sudo ./servicerouter.py --marathon http://localhost:8080 --haproxy-config /etc/haproxy/haproxy.cfg")

def main():
	app_name = argv[1]
	number_instance = int(argv[2])
	while True:
		try:
			containers_name = getContainersName(app_name)
			avg_cpu = avgCPUUsage(containers_name)
			print ("Avg cpu usage:"+str(avg_cpu))
			if(avg_cpu > 0.4):
				if(number_instance < 10):
					number_instance += 1
					scale(app_name, number_instance)
					print('sacle: scale up microbot to: '+ str(number_instance))
					print("sleep 30s...")
					time.sleep(30)
			elif(avg_cpu < 0.2):
				if(number_instance > 1):
					number_instance -= 1
					scale(app_name, number_instance)
					print('sacle: scale down microbot to: '+ str(number_instance))
					print("sleep 30s...")
					time.sleep(30)
		except Exception as e:
			print(e)
		finally:
			time.sleep(5)
if __name__ == '__main__':
    main()





	

