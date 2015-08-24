#Hướng dẫn sử dụng hệ thống auto-scale
**Yêu cầu**: Máy đã được cài đặt docker, haproxy, python3.

**Bước 1**: Vào thư mục ScaleServer chạy ```docker-compose up -d``` để khởi động các dịch vụ của hệ thống auto-scale

**Bước 2**: Vào thư mục run-app chạy lệnh ```./marathon.py post microbot``` để khởi chạy một ứng dụng.
- Thêm về cách sử dụng: 
	+ ```./marathon.py post <file-name>```: chạy một ứng dụng mà các tham số được định nghĩa trong file json: <file-name>.json sau đó cấu hình lại file config của haproxy.
	+ ```./marathon.py put <app-name> <number-intance>```: sacle ứng dụng có tên <app-name> tới số intance là <number-intance>, sau đó cấu hình lại file config của haproxy.

**Bước 3**: Vào thư mục scale chạy lệnh ```./autoscale.py <app-name> <number-intance>``` để thực hiện auto scale ứng dụng có tên app-name với số lượng intance đang có là number-intance.

Good luck!
