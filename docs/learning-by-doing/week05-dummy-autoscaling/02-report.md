# Báo cáo tuần 5
#### Auto - scaling team

##### Xây dựng hệ thống auto-scaling giả

**1. Ý tưởng**
- Sử dụng cAdvisor để thu thập thông tin và InfluxDB để lưu thông tin.
- Dùng thư viện Client Libraries hỗ trợ python có sẵn của InfluxDB để lấy thông tin.
_  Chạy một docker container, theo dõi, cài đặt thuật toán threshold, thực hiện lệnh scale đơn giản bằng việc in ra màn hình dòng thông báo.
_ Dùng python.

**2. Thực hiện**
- Code
```sh
import time
from time import gmtime, strftime
from influxdb.influxdb08 import InfluxDBClient
###
THRESHOLD_UP = 0.002
THRESHOLD_DOWN = 0.001
HOST = 'localhost'
PORT = 8086
USER = 'root'
PASS = 'root'
DATABASE = 'cadvisor'
SELECT = 'derivative(cpu_cumulative_usage)'
SERIES = "'stats'"
WHERE = 'container_name =~ /.*admiring_leakey.*/ and time>now()-5m'
GROUP_BY = "time(5s), container_name"
CONDITION = "limit 1 "

###
client = InfluxDBClient(HOST,PORT,USER,PASS,DATABASE)
query = "select"+SELECT+"from"+SERIES+"where"+WHERE+"group by "+GROUP_BY+CONDITION

while True:
    result = client.query(query)
    result = result[0]
    result = result[u'points'][0][1]
    result = result/10**9/4
    currentTime=strftime("%Y-%m-%d %H:%M:%S", gmtime())

    if(result>THRESHOLD_UP):
        print currentTime+" CPU_USAGE= "+str(result)+" scalling up, add 1 instance"
        THRESHOLD_UP=THRESHOLD_UP
    elif(result<THRESHOLD_DOWN):
        print currentTime+" CPU_USAGE= "+str(result)+" scalling down, turn off 1 instance"
        THRESHOLD_DOWN=THRESHOLD_DOWN


    time.sleep(5)
```

- Có thể thay đổi ngưỡng threshold_up, threshold_down cho phù hợp
- Tự động cập nhật lại threshold khi thực hiện scaling.
- Theo dõi docker container theo chu kì 5 phút và đưa ra quyết định scale

![image](https://github.com/tranhuucuong91/autoscaling/blob/master/docs/learning-by-doing/week05-dummy-autoscaling/images/15.png)