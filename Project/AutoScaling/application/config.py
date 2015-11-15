"""Config for autoscale.py
author: cuongnb14@gmail.com
"""
CONFIG = {

	# Config influxdb host
	"INFLUXDB" : {
		"host": "localhost",
		"port" : "8086",
		"username" : "root",
		"password" : "root",
		"db_name" : "cadvisor",
		"ts_mapping" : "mapping"
	},

	# Config marathon host
	"MARATHON" : {
		"host" : "localhost",
		"port" : "8080"
	},

	# Config times 
	# w_config_ha: time wait to config haproxy.cfg affter scale

	"TIME" : {
		"w_config_ha" : 30,
		"v_up" : 5,
		"after_scale" : 30,
		"v_down" : 5,
		"monitor" : 60
	},

	"MARIA_RESTFUL" : {
		"host": "localhost",
		"port": 4000
	}
}