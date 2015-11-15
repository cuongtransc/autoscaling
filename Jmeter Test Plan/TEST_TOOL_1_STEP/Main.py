__author__ = 'huanpc'
import os
import constant
import config
import time
from sys import argv
from random import randint
import MySQLdb

def getID():
    '''
    Ham nay bo
    :return:
    '''
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

def getCustomerRecordFromDB():
    '''
    Tao du lieu dang ky tai khoan nguoi dung
    address_id,customer_id,firstname,lastname,company,address_1,address_2,city,postcode,country_id,zone_id
    :return:
    '''
    try:
        i = 0
        f = open(config.CSV_FILE_PATH_2, 'w')
        db = MySQLdb.connect(host=config.HOST,port=config.PORT, user=config.USER, passwd=config.PASSWORD,db=config.DB)
        cur = db.cursor()
        cur.execute("SELECT opencart.oc_customer.email,oc_address.* FROM opencart.oc_address, "
                    "opencart.oc_customer where "+
                    "oc_customer.customer_id = oc_address.customer_id")
        results = cur.fetchall()
        if results == None:
            return False
        for record in results:
            i +=1
            data = list()
            data.append(str(record[0]))
            data.append(str(constant.RAW_PASSWORD))
            data.append(str(record[1]))
            data.append(str(record[2]))
            data.append(str(record[3]))
            data.append(str(record[4]))
            data.append(str(record[5]))
            data.append(str(record[6]))
            data.append(str(record[7]))
            data.append(str(record[8]))
            data.append(str(record[9]))
            data.append(str(record[10]))
            data.append(str(record[11]))
            line = ','.join(data)
            f.write(line + '\n')
        f.close()
        return True
    except:
        return False


def truncate_table():
    """
    Xoa du lieu truoc khi chay test plan
    :return:
    """
    db = MySQLdb.connect(host=config.HOST,port=config.PORT, user=config.USER, passwd=config.PASSWORD,db=config.DB)
    cur = db.cursor()
    cur.execute("DELETE FROM "+config.TABLE_ADDRESS)
    results = cur.fetchall()
    if results == None:
        return False
    cur.execute("DELETE FROM "+config.TABLE_CUSTOMER)
    results = cur.fetchall()
    if results == None:
        return False
    cur.execute("DELETE FROM oc_order ")
    results = cur.fetchall()
    if results == None:
        return False
    cur.execute("DELETE FROM oc_order_history ")
    results = cur.fetchall()
    if results == None:
        return False
    cur.execute("DELETE FROM oc_customer_login")
    results = cur.fetchall()
    if results == None:
        return False
    cur.execute("DELETE FROM oc_customer_activity")
    results = cur.fetchall()
    if results == None:
        return False
    cur.execute("DELETE FROM oc_customer_ip")
    results = cur.fetchall()
    if results == None:
        return False
    return True

def createRegisterData():
    '''
    Tao du lieu dang ky tai khoan nguoi dung
    # customer_group_id,firstname,lastname,email,
    # telephone,fax,company,address_id,address_1,address_2,city,postcode,
    # country_id,zone_id,password,confirm,newsletter,agree
    :return:
    '''
    try:
        ids = getID()
        customer_id = ids[0]
        address_id = ids[1]
        first_name_list = constant.FIRST_NAME
        last_name_list = constant.LAST_NAME
        i = 0
        f = open(config.CSV_FILE_PATH_1, 'w')
        row = ['',constant.CUSTOMER_GROUP_ID, ' ', ' ', ' ', ' ', ' ', constant.COMPANY, '',constant.ADDRESS_1,
               constant.ADDRESS_2,
               constant.CITY, constant.POSTCODE, constant.COUNTRY_ID, constant.ZONE_ID,
               constant.RAW_PASSWORD, constant.CONFIRM, constant.NEWSLETTER, constant.AGREE]
        while i < config.NUM_OF_THREADS:
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
        return True
    except:
        return False

def get_param(x):
    '''
    Doc stdin
    :param x:
    :return:
    '''
    return {
        '10': 10,
        '100': 100,
        '1000': 1000,
        '10000': 10000,
    }.get(x, 10)    # 9 is default if x not found

def main():
    config.NUM_OF_THREADS = get_param(argv[0])
    print 'Number of threads: '+str(config.NUM_OF_THREADS)
    # Truncate table
    if truncate_table() == False:
        print 'Truncate Table Error !'
        return
    # Tao du lieu dang ky nguoi dung
    if createRegisterData()==False:
        print 'Make Register Data Error !'
        return

    if os.system(config.RUN_JMETER_1) != 0:
        return
    print 'Register Test Plan done !'

    # Tao du lieu Order
    if getCustomerRecordFromDB()==False:
        print 'Make Order Data Error !'
        return

    time.sleep(config.TIME_DELAY)

    # Run Order Jmeter Test Plan
    if os.system(config.RUN_JMETER_2) != 0:
        return
    print 'Order Test Plan done !'

if __name__ == '__main__':
    main()
