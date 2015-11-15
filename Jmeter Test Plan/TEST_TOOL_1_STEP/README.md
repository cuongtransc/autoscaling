## Tool tự động sinh dữ liệu  + chạy kịch bản test
1. Copy folder TEST_TOOL_1_STEP vào folder `/apache jmeter/`, ngang cấp với folder `/bin`
2. Vào TEST_TOOL_1_STEP/config.py sửa lại số luồng cần test, username, password của opencart database
3. `python TEST_TOOL_1_STEP/Main.py [Number of threads]` để chạy
4. Lưu ý:
- Hiện tại tham số `Number of threads` chỉ hỗ trợ các giá trị 10,100,1000,10.000
