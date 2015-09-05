from sys import argv
import json
from influxdb.influxdb08 import InfluxDBClient
import time
import http.client
import os

connect = http.client.HTTPConnection("localhost:8080")
connect.request('GET','/v2/apps/microbot')
response = connect.getresponse()
json_response = response.read().decode("utf-8")
obj_response = json.loads(json_response)
tasks = obj_response['app']['tasks']
containers_name = []
for task in tasks:
	print(task['id'])