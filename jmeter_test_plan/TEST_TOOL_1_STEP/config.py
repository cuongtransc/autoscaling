__author__ = 'huanpc'
########################################################################################################################
HOST = "25.22.28.94"
PORT = 3307
USER = "root"
PASSWORD = "root"
DB = "opencart"
TABLE_ADDRESS = 'oc_address'
TABLE_CUSTOMER= 'oc_customer'
########################################################################################################################
DIR_OUTPUT_PATH = './Test_plan'
# So ban ghi can tao
NUM_OF_THREADS = 10
OPENCART_PORT = 10000
RAM_UP = 10
CONFIG_FILE_PATH = DIR_OUTPUT_PATH+'/config.csv'
TEST_PLAN_FILE_PATH_1 = DIR_OUTPUT_PATH+'/plan/Opencart_register_'+str(NUM_OF_THREADS)+'.jmx'
TEST_PLAN_FILE_PATH_2 = DIR_OUTPUT_PATH+'/plan/Opencart_order_'+str(NUM_OF_THREADS)+'.jmx'
CSV_FILE_PATH_1 = DIR_OUTPUT_PATH+'/register_infor.csv'
CSV_FILE_PATH_2 = DIR_OUTPUT_PATH+'/order_infor.csv'
RESULT_FILE_PATH_1 = './Test_plan/result1.jtl'
RESULT_FILE_PATH_2 = './Test_plan/result2.jtl'
RUN_JMETER_1 = 'sh ../bin/jmeter -n -t '+TEST_PLAN_FILE_PATH_1+' -l '+RESULT_FILE_PATH_1
RUN_JMETER_2 = 'sh ../bin/jmeter -n -t '+TEST_PLAN_FILE_PATH_2+' -l '+RESULT_FILE_PATH_2
TIME_DELAY = 5
########################################################################################################################