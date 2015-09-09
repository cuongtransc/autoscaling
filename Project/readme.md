# Cài đặt hệ thống auto scaling
**Yêu cầu:** Máy đã được cài đặt docker, haproxy, python3.
1. Vào thư mục application và thực hiện lệnh: `docker-compose up -d` để khởi động các dịch vụ của hệ thống auto-scale
2. Sử dụng `./marathon/marathon.py` để khởi chạy một ứng dụng:
- `./marathon.py post <file-name>`: chạy một ứng dụng với các tham số được định nghĩa trong file json: file-name.json sau đó cấu hình lại file haproxy.cfg của haproxy.
- `./marathon.py put <app-name> <number-intance>`: scale ứng dụng có tên `app_name` tới số intance là `number_intance`, sau đó cấu hình lại file haproxy.cfg của haproxy.
3. Chạy RESTful API server bằng câu lệnh `maria/restfulapi.py` để tương tác với mariadb (chứa các luật của các ứng dụng)
4. Chạy `./autoscale.py <app-name>` để thực hiện auto scale ứng dụng có tên `app-name`
