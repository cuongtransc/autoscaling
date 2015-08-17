# Báo cáo tuần 4
#### Auto - scaling team

##### A. Setup hệ thống monitoring.
**1. Setup InfluxDB – bộ Database chuyên hóa.**
- script:
```sh
$ docker run -d -p 8083:8083 -p 8086:8086 --expose 8090 --expose 8099 -e     PRE_CREATE_DB=cadvisor --name influxsrv tutum/influxdb:0.8.8
```
- port 8083: giao diện tương tác trực quan cho người dùng
- port 8086: giao tiếp với các application khác
- Setup thành công:
    + vào địa chỉ localhost:8083
    + ![Image 1](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/01.png)
        - username - password : root
    +  giao diện người dùng:
    + ![Image 2](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/02.png)

        Nếu chưa có bộ database cadvisor  thì tạo mới 1 bộ.

**2. Setup cAdvisor - bộ sensor**
- Script:
```sh
docker run \
--volume=/:/rootfs:ro \
--volume=/var/run:/var/run:rw \
--volume=/sys:/sys:ro \
--volume=/var/lib/docker/:/var/lib/docker:ro \
--publish=8080:8080 \
--link=influxsrv:influxsrv	\
--detach=true \
--name=cadvisor \
google/cadvisor:0.14.0 \
-storage_driver=influxdb \
-storage_driver_db=cadvisor \
-storage_driver_host=influxsrv:8086
```
+ cổng giao diện người dùng: 8080:8080
+ các thông số khác thiết lập như trên
- setup thành công:
    + vào link localhost:8080
    + ![Image 3](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/03.png)
    + ![Image 4](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/04.png)

**3. Setup Grafana - bộ visualizing**
- Script:
```sh
docker run -d -p 3000:3000 \
-e HTTP_USER=admin \
-e HTTP_PASS=admin \
-e INFLUXDB_HOST=localhost \
-e INFLUXDB_PORT=8086 \
-e INFLUXDB_NAME=cadvisor \
-e INFLUXDB_USER=root \
-e INFLUXDB_PASS=root \
--link=influxsrv:influxsrv	\
grafana/grafana:2.0.2
```
+ listen ở cổng 3000
+ giao tiếp với InfluxDB ở cổng 8086
- setup thành công:
    + vào link localhost:8086
    + user – password: admin
    + ![image 5](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/05.png)
    + ở giao diện chính, click vào logo Grafana góc trái trên cùng màn hình, popup hiện ra chọn Data Sources, Add New
    + ![image 6](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/06.png)
    + setup các thông số như sau:
    + ![image 7](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/07.png)
- Cấu hình Grafana để theo dõi các statistics:
    + Ở menu bên phải chọn Dashboard,  Home Menu, New, Add Panel, Graph
    + ![image 8](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/08.png)
    + một Graph hiện ra, chọn no title, edit
    + ![image 9](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/09.png)
    + 1 bảng hiện ra, thiết lập các query  để lấy dữ liệu thích hợp từ InfluxDB
    + Ví dụ:
    + ![image 10](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/10.png)
    + ![image 11](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week04-docker-monitoring/images/11.png)

#### Overview

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
--|--|--|--|--|--|--|--|--|--|--|--|--|--|--

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
    VD:
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

#### References
- https://www.brianchristner.io/how-to-setup-docker-monitoring/
