
__author__ = 'huanpc'

import constant
import config
import argparse
from random import randint
import MySQLdb


#register
# customer_id,customer_group_id,firstname,lastname,email,
# telephone,fax,company,address_id,address_1,address_2,city,postcode,
# country_id,zone_id,password,confirm,newsletter,agree

# make order
# address_id,firstname,lastname,company,address_1,
# address_2,city,postcode,country_id,zone_id, email, password

def getID():
    db = MySQLdb.connect(host=config.HOST,port=config.PORT, user=config.USER, passwd=config.PASSWORD,db=config.DB)
    cur = db.cursor()
    cur.execute("SELECT customer_id FROM "+config.TABLE_CUSTOMER+" order by customer_id desc limit 1")
    tm = cur.fetchone()
    if tm == None:
        customer_id_begin  = 0
    else:
        customer_id_begin = tm[0]
    cur.execute("SELECT address_id FROM "+config.TABLE_ADDRESS+" order by address_id desc limit 1")
    tm = cur.fetchone()
    if tm == None:
        address_id_begin = 0
    else:
        address_id_begin = tm[0]
    return [customer_id_begin,address_id_begin]

# Tao du lieu nguoi dung
def createCustomerInforData():
    ids = getID()
    customer_id = ids[0]
    address_id = ids[1]
    first_name_list = constant.FIRST_NAME
    last_name_list = constant.LAST_NAME
    i = 0
    f = open(config.DIR_OUTPUT_PATH + '/customer_infor.csv', 'w')
    row = ['',constant.CUSTOMER_GROUP_ID, ' ', ' ', ' ', ' ', ' ', constant.COMPANY, '',constant.ADDRESS_1,
           constant.ADDRESS_2,
           constant.CITY, constant.POSTCODE, constant.COUNTRY_ID, constant.ZONE_ID,
           constant.RAW_PASSWORD, constant.CONFIRM, constant.NEWSLETTER, constant.AGREE]
    while i < config.NUM_OF_ROWS:
        customer_id +=1
        address_id +=1
        first_name = first_name_list[randint(0, len(constant.FIRST_NAME) - 1)]
        last_name = last_name_list[randint(0, len(constant.LAST_NAME) - 1)]
        row[0] = str(customer_id)
        row[2] = first_name
        row[3] = last_name
        row[4] = str(first_name + '.' + last_name + '@gmail.com').lower()
        row[5] = str(randint(11111, 99999)) + str(randint(11111, 99999))
        row[6] = row[5]
        row[8] = str(address_id)
        line = ','.join(row)
        i += 1
        f.write(line + '\n')
    f.close()

# def createProductData():
# Tao du lieu mau khi dang ky tai khoan
# customer_group_id# firstname# lastname# email# telephone
# fax# company# address_1# address_2# city# postcode# country_id
# zone_id# password# confirm# newsletter# agree


def main():
    # parser = argparse.ArgumentParser(description='Sinh du lieu mau cho tap test')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                help='an integer for the accumulator')

    createCustomerInforData()


if __name__ == '__main__':
    main()
