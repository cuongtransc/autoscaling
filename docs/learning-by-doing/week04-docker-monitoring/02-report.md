<<<<<<< HEAD
# Báo cáo tuần 4 - 5
#### Auto - scaling team
##### Setup hệ thống monitoring.
**1. Setup InfluxDB – bộ Database chuyên hóa.**
- script:
```sh
$ docker run -d -p 8083:8083 -p 8086:8086 --expose 8090 --expose 8099 -e     PRE_CREATE_DB=cadvisor --name influxsrv tutum/influxdb:0.8.8
```
- port 8083: giao diện tương tác trực quan cho người dùng
- port 8086: giao tiếp với các application khác
- Setup thành công:
    + vào địa chỉ localhost:8083
    + ![Image 1]()
        - username - password : root
    +  giao diện người dùng: 
    + ![Image 2]()
    
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
    + ![Image 3]()
    + ![Image 4]()
    
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
    + ![image 5]()
    + ở giao diện chính, click vào logo Grafana góc trái trên cùng màn hình, popup hiện ra chọn Data Sources, Add New
    + ![image 6]()
    + setup các thông số như sau:
    + ![image 7]()    
- Cấu hình Grafana để theo dõi các statistics:
    + Ở menu bên phải chọn Dashboard,  Home Menu, New, Add Panel, Graph
    + ![image 8]()      
    + một Graph hiện ra, chọn no title, edit
    + ![image 9]()      
    + 1 bảng hiện ra, thiết lập các query  để lấy dữ liệu thích hợp từ InfluxDB
    + Ví dụ:
    + ![image 10]()      
    + ![image 11]()      
    
##### Các câu hỏi về hệ thống monitoring
**1. cAdvisor**
- Cấu trúc dữ liệu
    + Theo dõi theo process, dưới dạng cấu trúc cây (có root, các nút...)
    + Theo dõi các thông số sau:
        + CPU: total usage, usage per core, usage breakdown, đơn vị tính theo số core, một core thật tương ứng được chia làm 10^9 core đơn vị
        + Memory:total usage(MB)
        + Network: Throughput-Tx bytes,Rx bytes (Bytes per second), Errors(Errors per second) - Tx bytes, Rx bytes
        + Filesystem: GB usage
- Tần suất gửi dữ liệu
    + Dữ liệu được thu thập và xử lý theo chu kì 10s
- Ước lược kích thước dữ liệu/ 1 docker container
    + Ước lượng theo công thức:
    
        >kích thước một đơn vị dữ liệu mẫu * tần suất gửi dữ liệu trong một đơn vị thời gian* thời gian theo dõi tính theo một đơn vị thời gian
+ Một đơn vị dữ liệu mẫu bao gồm các trường:

Time|Sequence_number|fs_limit|Machine|memory_usage|container_name|cpu_cumulative_usage|memory_working_set|rx_bytes|tx_errors|tx_bytes|fs_device|rx_errors|fs_usage
--|--|--|--|--|--|--|--|--|--|--|--|--|--|

**2. InfluxDB**
- Cách tổ chức cấu trúc database
    + Lưu trữ dữ liệu theo mốc thời gian time series
    + Một times series gồm có 3 trường time (giá trị tự động micro s), sequence_number (giá trị tự điền), column (có thể set value)
    + Có thể thêm nhiều column cho một time series → thuận tiện cho việc ghi exception, event
    + Được thiết kế để tối ưu việc lưu trữ và truy xuất một lượng lớn dữ liệu theo dòng thời gian
- Các cách truy vấn cung cấp
    + Gộp theo nhóm
    + Truy vấn theo time series
    + Gộp nhiều series để truy vấn
    + Gộp theo thời gian (group by time)
    + Cung cấp biểu đồ kết quả trả về trực quan
    + Cung cấp các aggregate function: sum, mean, max, count...
- Ngôn ngữ truy vấn
    + Tương tự SQL
    + Có hỗ trợ thêm truy vấn theo khoảng thời gian, mốc thời gian
    + Hỗ trợ đọc và ghi dữ liệu dùng các giao thức HTTP POST, GET
    + Aggregate function
    + Continuous query: xử lý 1 nhóm dữ liệu theo chu kì và lưu vào database
    ```sh
    VD:
    select count(type) from events group by time(10m), type 
    into events.count_per_type.10m
    ```
- Thư viện “Client Libraries”
    + Cung cấp các Client API để thực hiện đọc, ghi, truy vấn đến InfluxDB với nhiều ngôn ngữ:
    javaScript, Ruby, Rails, Python, PHP, Perl, .NET... 

**3. Grafana:**
- Những biểu đồ cung cấp:
    + graph
        + ![Image]()
    + singlestat
        + ![Image]()
    + annotation
        + ![Image]()
- Việc aggregate dữ liệu
    + Hỗ trợ tạo query đến InfluxDB để lấy dữ liệu
    + Hỗ trợ query template
    + Hỗ trợ các aggregate function của InfluxDB
    + Có thể aggregate theo mốc thời gian, khoảng thời gian
- API để lấy dữ liệu tổng hợp
    + Các API viết bằng javascript để truy vấn đến InfluxDB qua giao thức HTTP
### Xây dựng hệ thống auto-scaling giả

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


	













=======
TODO
>>>>>>> 763b05e510364ca39f458f38a4c1d480e3159350
