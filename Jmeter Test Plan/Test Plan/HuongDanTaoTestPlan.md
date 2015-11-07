## About	
Doc hướng dẫn việc tạo ra thiết lập file OpenCart.jmx

## Xây dựng kịch bản test
### Kịch bản test bao gồm các bước:
1. Register.
2. Login.
3. Order by Guest.
4. Order by User.

### Yêu cầu của việc thực hiện test trên Jmeter là đã thực hiện sinh dữ liệu ra file csv. File csv bao gồm các cột, với thông tin trên từng cột lần lượt là
1. customer_id
2. customer_group_id
3. firstname
4. lastname
5. email
6. telephone
7. fax
8. company
9. address_id
10. address_1
11. address_2
12. city
13. postcode
14. country_id
15. zone_id
16. password
17. confirm
18. newsletter
19. agree

### Hướng dẫn cách record lại các bước bằng cách thiết lập proxy
Cơ chế của việc này là tạo một proxy ở localhost (tạo bằng Jmeter), sau đó config proxy ở trình duyệt, việc thực hiện request sẽ đều đi qua proxy này và được ghi lại bằng Jmeter. 
#### Sau đây là hướng dẫn record thiết đặt proxy để ghi lại kịch bản test.
##### Thiết lập Jmeter
1. Mở Jmeter lên
2. Lựa chọn "TestPlan"
![alt text][1]
3. Bấm chuột phải vào "Test Plan" và thêm một threa group mới: Add > Threads (Users) > Thread Group
![alt text][3]
4. Lựa chọn Thread Group
5. Bấm chuột phải và chọn "Add > Config Element > HTTP Request Defaults"
![alt text][5]
6. Ở trong HTTP Request Default vừa tạo. Điền "localhost" vào Servername or IP. (HTTP Request Default sẽ thiết lập thông số mặc định cho các HTTP Request - cùng hoặc trong các scope nhỏ hơn).
![alt text][6]
7. Path: Để trống
8. Chuột phải vào "Thread Group" và thêm recording controller: Add > Logincontroller > Recording Controller (các thông tin mà ta ghi đc sẽ nằm trong controller này)
![alt text][8]
9. Chọn WorkBench
10. Chuột phải vào wordbench và thêm một recorder: Add -> Non-Test Elements -> HTTP(S) Test Script Recorder
![alt text][10]
11. Trong phần HTTP(S) Test Script Recorder, bỏ trống nếu muốn ghi lại tất cả các hành động của trang web (mình bỏ trống). 
12. Chuột phải vào "HTTP(S) Test Script Recorder" va thêm listener: Add -> Listerner -> View Result Tree
![alt text][12]
13. Trở về chõ "HTTP(S) Test Script Recorder" và bấm nút "Start" ở cuối trang. (port trong HTTP(S) TS để là 8080)

![alt text][13]
Nếu gặp lỗi về certificate, thực hiện theo link sau:
http://jmeter.apache.org/usermanual/component_reference.html#HTTP%28S
%29_Test_Script_Recorder

##### Thiết lập browser để sử dụng Jmeter Proxy
Trong bài viết này mình sử dụng FireFox (new 5/11/2015). 
14. Khởi động FireFox
15. Từ thanh công cụ, chọn Edit > Preferences
16. Lựa chọn Advance tag. Trong thẻ Network chọn setting.
17. Lựa chọn "Manual proxy configuration"
18. Thiết lập. HTTP Proxy: localhost và Port: 8080. Port trùng với port trong khi thiết lập ở Jmeter.
![alt text][18]
19. Ok, finish. Giờ là lúc chạy test. Hãy vào thử 1 trang web bằng firefox xem có chuyện gì xảy ra.
![alt text][19]


[1]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/1.png
[3]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/3.png
[5]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/5.png
[6]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/6.png
[8]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/8.png
[10]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/10.png
[12]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/12.png
[13]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/13.png
[18]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/18.png
[19]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/19.png



### Kịch bản cho Register
Tư tưởng: tạo dữ liệu mẫu rồi lưu bằng file csv, rồi lấy thông tin từ file csv, sau đó truyền vào để thực hiện register. 
sau đây là các bước cặn kẽ trong Kịch bản Register.

1. Trước tiên sử dụng proxy + tay để tạo ra được cấu trúc TestPlan như hình dưới. Trong hình ta thấy được là chúng ta đẵ đặt biên cho toàn bộ TestPlan là HOST:localhost và port:80

![alt text][21]

2. Thực hiện import csv và đưa nó ra thành các biến toàn cục

![alt text][22]

3. Cài đặt HTTP Request Default.

![alt text][23]

4. Load trang chủ

![alt text][24]

5. Các request mà brower gửi đi khi load form.

![alt text][25]

6. Phương thức POST gửi các thông tin đi.

![alt text][26]

7. Chuyển hướng khi register thành công

![alt text][28]

8. Chuyển hướng khi logout

![alt text][29]


Để thực hiện chạy test, chạy lệnh #### CTR + R


[21]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/21.png
[22]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/22.png
[23]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/23.png
[24]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/24.png
[25]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/25.png
[26]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/26.png
[28]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/28.png
[29]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/29.png

## How to make Test Plan with Jmeter
1. Ghi lại request + parameter bằng HTTP Script Recording
2. Tạo Register test case
3. Tạo Make Order test case
4. .....

### Tạo kịch bản Make Order với trường hợp khách hàng có tài khoản.
`Yêu cầu: Người dùng đã có tài khoản`
1. Dùng `HTTP(S) Test Script Recorder + Recording Controller`  để ghi lại định dạng các request cần thực hiện. ![image][30]
2. Các tham số để tạo request lấy từ bộ dữ liệu csv đã tạo . ![image][31]
3. Điền tham số `username`, `password ` vào Login Post request ![image][32]
4. Tạo  `If controller `để thực hiện rẽ nhánh theo từng  trạng thái của Login request ở trên.
 - Nếu Login thành công, thực hiện nhánh ![image][33]
    - Điền các tham số hóa vào trường Parameters ![image][35]
 - Nếu Login thất bại, thực hiện nhánh 2 ![image][34]
5. Dùng `Aggregate Report + Aggregate Graph` để thống kê các request thành công, thất bại, tốc độ trung bình ... ![image][36]	

[30]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/30.png
[31]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/31.png
[32]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/32.png
[33]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/33.png
[34]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/34.png
[35]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/35.png
[36]: https://github.com/tranhuucuong91/autoscaling/blob/master/Jmeter%20Test%20Plan/Test%20Plan/images/36.png


