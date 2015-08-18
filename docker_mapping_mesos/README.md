# Mapping DockerId to MesosId
Get docker container name and Mesos task id, then store in **InfluxDB**.

| table   | column 1       | column 2      |
| ------- | -------------- | ------------- |
| mapping | container_name | mesos_task_id |

## Build
```bash
docker build --tag=cocu/docker-mapping-mesos:0.1 .
```

## Run
```bash
docker run -d \
    -v /var/run/docker.sock:/var/run/docker.sock \
    cocu/docker-mapping-mesos:0.1
```

## Default Variables
- INFLUXDB_HOST=localhost
- INFLUXDB_PORT=8086
- INFLUXDB_NAME=cadvisor
- INFLUXDB_USER=root
- INFLUXDB_PASS=root
- TIME_INTERVAL=10
