__author__ = 'huanpc'

import constant
import argparse
from random import randint
# Duong dan toi thu muc output file dataseed
DIR_OUTPUT_PATH = './output'
# Chon gia tri cho id trong bang customer
customer_id_begin = 5
product_id_begin = 0
# So ban ghi can tao
num_of_row = 100

#def createProductData():
# Tao du lieu mau khi dang ky tai khoan
# customer_group_id# firstname# lastname# email# telephone
# fax# company# address_1# address_2# city# postcode# country_id
# zone_id# password# confirm# newsletter# agree

def createRegisterInforData():
    first_name_list = constant.FIRST_NAME
    last_name_list = constant.LAST_NAME
    i = 0
    f = open(DIR_OUTPUT_PATH+'/register_data_seed.csv','w')
    row = [constant.CUSTOMER_GROUP_ID,' ',' ',' ',' ',' ',constant.COMPANY,constant.ADDRESS_1,constant.ADDRESS_2,
           constant.CITY,constant.POSTCODE,constant.COUNTRY_ID,constant.ZONE_ID,
           constant.PASSWORD,constant.CONFIRM,constant.NEWSLETTER,constant.AGREE]
    while i<num_of_row:
        first_name = first_name_list[randint(0,len(constant.FIRST_NAME)-1)]
        last_name = last_name_list[randint(0,len(constant.LAST_NAME)-1)]
        row[1] = first_name
        row[2] = last_name
        row[3] = str(first_name+'.'+last_name+'@gmail.com').lower()
        row[4] = str(randint(11111,99999))+ str(randint(11111,99999))
        row[5] = row[4]
        line = ','.join(row)
        i+=1
        f.write(line+'\n')
    f.close()

# Tao du lieu nguoi dung day du
def createCustomerData():
    first_name_list = constant.FIRST_NAME
    last_name_list = constant.LAST_NAME
    i = 0
    f = open(DIR_OUTPUT_PATH+'/customer_data_seed.csv','w')
    column_heading = ['customer_id','customer_group_id','store_id','first_name','last_name','email','telephone','fax','password','salt','cart','whistlist',
                      'newsleter','address_id','custom_field','ip','status','approves','safe','token','date_added']
    row = ['1',constant.CUSTOMER_GROUP_ID,constant.STORE_ID,'1','1','1','1','1',constant.PASSWORD,constant.SALT,constant.CART,constant.WHISTLIST,constant.NEWSLETTER,constant.ADDRESS_ID,
           constant.CUSTOM_FIELD,constant.IP,constant.STATUS,constant.APPROVED,constant.SAFE,constant.TOKEN,constant.DATE_ADDED]
    while i<num_of_row:
        first_name = first_name_list[randint(0,len(constant.FIRST_NAME)-1)]
        last_name = last_name_list[randint(0,len(constant.LAST_NAME)-1)]
        row[0] = str(i+customer_id_begin)
        row[3] = first_name
        row[4] = last_name
        row[5] = str(first_name+'.'+last_name+'@gmail.com').lower()
        row[6] = str(randint(11111,99999))+ str(randint(11111,99999))
        row[7] = row[6]
        line = ','.join(row)
        i+=1
        f.write(line+'\n')
    f.close()

def main():
    # parser = argparse.ArgumentParser(description='Sinh du lieu mau cho tap test')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                help='an integer for the accumulator')
    createRegisterInforData()

if __name__ == '__main__':
    main()
