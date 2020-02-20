#!/usr/bin/env python3
import requests
import json
import socket  
import pymysql
import ipaddress

# 檢查是否支援IPv6 function
def checkIPv6(domain, port):
    res = socket.getaddrinfo(domain, port, 0, 0, socket.SOL_TCP)

    if ipaddress.ip_address(res[0][4][0]).version == 6:
        check = domain + ":" + port + " 支援IPv6，" + "IPv6為" +  res[0][4][0]
        status = 'ok'
    else:
        check = domain + ":" + port + " 不支援IPv6"
        status = 'error'

    return check, status

# 查詢有在使用中的domain function
def queryDomainResult(mysqlIP, user, password):
    db_test = pymysql.connect(mysqlIP, user, password, "hoster_db")
    cursor = db_test.cursor()

    sql = "SELECT * FROM `domain` WHERE `enable` = '1'"

    try:
       cursor.execute(sql)
       results = cursor.fetchall()
    except:
       print ("Error: unable to fetch data")

    db_test.close()

    return results


# 驗證本機是否開啟IPv6
r = requests.get("http://ifconfig.co/ip")

myIP = r.text.strip('\n')

if ipaddress.ip_address(myIP).version == 6:
    print("本機IPv6為", myIP)
else:
    print("請先開啟本機IPv6")
    exit()

# 開始檢查
results = queryDomainResult("資料庫IP","資料庫帳號","資料庫密碼")

for row in results:
    domain = row[1]
    check, status = checkIPv6(domain, "443")
