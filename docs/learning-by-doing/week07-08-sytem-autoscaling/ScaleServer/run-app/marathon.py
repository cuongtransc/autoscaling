#! /usr/bin/env python3
import http.client
import json
from sys import argv
import os

HOST_NAME = 'localhost:8080'
HEADER = {'Content-type': 'application/json'}

method = argv[1]
data = ""
url = ""
if method == 'put':
	data = '{"instances": '+ argv[3] +'}'
	url = '/v2/apps/' + argv[2]
else:
	f = open(argv[2]+'.json', 'r')
	data = json.load(f)
	data = json.dumps(data)
	url = '/v2/apps'


connect = http.client.HTTPConnection(HOST_NAME)
connect.request(method,url,data,HEADER)

response = connect.getresponse()
print(response.read().decode())
os.system("sudo ./servicerouter.py --marathon http://localhost:8080 --haproxy-config /etc/haproxy/haproxy.cfg")