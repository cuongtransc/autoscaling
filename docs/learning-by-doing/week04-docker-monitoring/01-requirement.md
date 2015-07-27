# Tìm hiểu và xây dựng hệ thống docker monitoring
**Thời gian**: 13/07/2015 - 19/07/2015

## Hệ thống monitor
Cần các thành phần:
1. **App agent (sensor)**: thu thập thông tin hệ thống, log và gửi đến bộ phận ghi nhận event.
2. **Ghi nhận event**: nhận các event từ agent và ghi vào database.
3. **Database event**: chuyên dụng, được thiết kế để tối ưu hóa việc lưu trữ dữ liệu event theo thời gian.
4. **Bộ phận tổng hợp, visualization**: aggregate, trực quan hóa dữ liệu event.

=> cần tìm kiếm một giải pháp tổng thể, tối ưu.
Có nhiều tiêu chí đánh giá. Cần liệt kê các tiêu chí, so sánh các giải pháp.

Tạm thời, tôi lựa chọn giải pháp:
1. **cAdvisor**: lấy thông tin cpu, ram của docker container.
2. **InfluxDB**: nhận dữ liệu từ cAdvisor và lưu trữ.
3. **Grafana**: truy vấn từ InfluxDB và visualization.

## Yêu cầu
### Setup hệ thống monitoring
Các bạn tham khảo các tài liệu sau:
1. https://www.brianchristner.io/how-to-setup-docker-monitoring/
2. http://blog.eddiekampe.se/posts/54ce4b94e4b0b3c7e59d165c
3. http://tech.trivago.com/2015/04/14/timeseries_influxdb/

### Trả lời các câu hỏi
1. **cAdvisor**: Cấu trúc dữ liệu, đơn vị đo, tần suất gửi dữ liệu, ước lượng về kích thước dữ liệu/một docker container.
2. **InfluxDB**: Cách tổ chức cấu trúc database. Cung cấp những cách truy vấn nào? Ngôn ngữ truy vấn?
3. **Grafana**: Cung cấp những biểu đồ nào? Cung cấp việc aggregate dữ liệu không? Và cung cấp api để lấy dữ liệu tổng hợp không?
