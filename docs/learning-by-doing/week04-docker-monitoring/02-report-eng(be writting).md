# Báo cáo tuần 4
#### Auto - scaling team

### A. Overview

**1. cAdvisor**

cAdvisor (Container Advisor) provides container users an understanding of the resource usage and performance characteristics of their running containers. It is a running daemon that collects, aggregates, processes, and exports information about running containers.

Specifically, for each container it keeps resource isolation parameters, historical resource usage, histograms of complete historical resource usage and network statistics. This data is exported by container and machine-wide.
- Performance Metrics:
    + CPU: total usage, usage per core, usage breakdown (Hz)
    + Memory: total usage(Byte)
    + Network: Throughput-Tx bytes,Rx bytes (Bytes per second), Errors(Errors per second) - Tx bytes, Rx bytes
    + Filesystem (Storage): total usage (Byte)
- Frequence of data collection: 
    + Real-time collector (per second)
- Size of data per one docker container measuring:

    >Size of a sample data unit *monitoring time by time unit * collected frequence of data 

+ Structure of a sample data unit:  

Time|Sequence_number|fs_limit|Machine|memory_usage|container_name|cpu_cumulative_usage|memory_working_set|rx_bytes|tx_errors|tx_bytes|fs_device|rx_errors|fs_usage
--|--|--|--|--|--|--|--|--|--|--|--|--|--|

**2. InfluxDB**

InfluxDB is a time series, metrics, and analytics database. cAdvisor only displays realtime information and doesn't store the metrics. We need to store the monitoring information which cAdvisor provides in order to display a time range other than realtime.

Feature:
- Time-Centric Functions
- Events
- Powerful Query Language
- Scalable Metrics
- Native HTTP API
- Built-in Explorer

Database structure:

+ By time series
+ Metrics data and events data oriented   
+ A sample time series record:

Time|Sequence_number|field 1|field 2|field 3|....
---|---|---|---|---|---

+ Store billions of data points.

Aggregate record:
+ Merge multiple series together 
+ Group by time range
+ Graph visualized 
+ Powerful aggregate function: sum, mean, max, count, median...
+ SQL-like query language

    ```sh
    Exam:
    select count(type) from events group by time(10m), type
    into events.count_per_type.10m
    ```
Client Libraries
 + Supporting to interact with InfluxDB throughout HTTP protocol (read, write,insert ...)
 + Support many language: javaScript, Ruby, Rails, Python, PHP, Perl, .NET...

Get more [here](https://influxdb.com/)

**3. Grafana:**

Grafana is a leading open source application for visualizing large-scale measurement data. The Grafana Dashboard allows us to pull all the pieces together visually. This powerful Dashboard allows us to run queries against the InfluxDB and chart them accordingly in a very nice layout.

Features:
+ graph

![Image](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/12.png)
+ singlestat
    
![Image](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/13.png)
+ annotation

![Image](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/14.png)

Data aggregate
+ Interacting with InfluxDB
+ Query template/ editor for InfluxDB

HTTP API
+ The Grafana backend exposes an HTTP API, the same API is used by the frontend to do everything from saving dashboards, creating users and updating data sources.

Get more [here](http://docs.grafana.org/)

### B. Installation of Docker Monitoring.
####1. Install the InfluxDb
- command:
```
$ docker run -d -p 8083:8083 -p 8086:8086 --expose 8090 --expose 8099 -e PRE_CREATE_DB=cadvisor --name influxsrv tutum/influxdb:0.8.8
```

+ `-p 8083:8083` : user interface, log in with username-admin, pass-admin
+ `-p 8086:8086` : interaction with orther application
+ `PRE_CREATE_DB=cadvisor` : create database have name `cadvisor`
+ `--name influxsrv` : container have name `influxsrv`, use to cAdvisor link it.
	
####2. Install the cAdvisor container and link it to the InfluxDB container.
- command:
```
docker run \
--volume=/:/rootfs:ro \
--volume=/var/run:/var/run:rw \
--volume=/sys:/sys:ro \
--volume=/var/lib/docker/:/var/lib/docker:ro \
--publish=8080:8080 \
--link=influxsrv:influxsrv  \
--detach=true \
--name=cadvisor \
google/cadvisor:0.14.0 \
-storage_driver=influxdb \
-storage_driver_db=cadvisor \
-storage_driver_host=influxsrv:8086 
```

+ `--publish=8080:8080` : user interface
+ `--link=influxsrv:influxsrv`: link to container influxsrv
+ `-storage_driver=influxdb`: set the storage driver as InfluxDB
+ Specify what InfluxDB instance to push data to:
	* `-storage_driver_host=influxsrv:8086 `: The *ip:port* of the database. Default is 'localhost:8086'
	* `-storage_driver_db=cadvisor `: database name. Uses db 'cadvisor' by default

- After install successfully access url `http://localhost:8080` You should now see the cAdvisor gathering statistics on your Docker host and containers

####3. Install the Grafana Dashboard and link it to the InfluxDB container:
- command:
```
docker run -d -p 3000:3000 \
-e HTTP_USER=admin \
-e HTTP_PASS=admin \
-e INFLUXDB_HOST=localhost \
-e INFLUXDB_PORT=8086 \
-e INFLUXDB_NAME=cadvisor \
-e INFLUXDB_USER=root \
-e INFLUXDB_PASS=root \
--link=influxsrv:influxsrv  \
grafana/grafana:2.0.2
```

- After install successfully access url `http://localhost:3000`, config to link it to the InfluxDb:
	+ Login: Username – admin, password – admin
	+ Click on the Grafana icon in the upper left hand corner of the GUI. Click on: Data Sources → Add New and fill information follow image:
	![Image](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/img01.png)

- Config to monitoring statistics: 
	+ Click Dashboard → Home Menu →  New →  Add Panel →  Graph
	![Image](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/img02.png)
	+ Click notitle → edit, after write our query for our graph at metric tab.
	![Image](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/img03.png)
	+ Example several graph:
	![Image](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/img04.png)



#### References
- https://www.brianchristner.io/how-to-setup-docker-monitoring/
- You can use json file to create dashboards: https://github.com/vegasbrianc/docker-monitoring
