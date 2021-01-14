#-*- coding = utf-8 -*-
#@Time:2020/11/21 23:21
#@Author:zdd
#@File:win.py
#@Software:PyCharm

import requests
from bs4 import BeautifulSoup
import json
import base64
from urllib.parse import quote
import pymysql

def dataget(username,password):
    session = requests.Session()
    r = session.get(
        url='https://mysso.cust.edu.cn/cas/login?service=https://jwgls1.cust.edu.cn/welcome')
    soup = BeautifulSoup(r.text, 'html.parser')
    execution = soup.find_all(name='input')[6]['value']
    formdata = {
        'username': username,
        'password': password,
        'execution': execution,
        '_eventId': 'submit',
        'geolocation': ''
    }
    r = session.post(
        url='https://mysso.cust.edu.cn/cas/login?service=https://jwgls1.cust.edu.cn/welcome', data=formdata)
    soup = BeautifulSoup(r.text, 'html.parser')
    r = session.get(
        url='https://portal.cust.edu.cn/custp/index')
    soup = BeautifulSoup(r.text, 'html.parser')
    r = session.get(url='https://mysso.cust.edu.cn/cas/login?service=https://jwgls1.cust.edu.cn/welcome',
                           allow_redirects=False)
    ticket = r.headers['Location'][42:]
    asp_net_sessionid_param = {'Ticket': ticket, 'Url': 'https://jwgls1.cust.edu.cn/welcome'}
    asp_net_sessionid_param = base64.b64encode(
        quote(json.dumps(asp_net_sessionid_param)).encode('utf-8')).decode('utf-8')
    asp_net_sessionid_param = {'param': asp_net_sessionid_param}
    headers = {'Content-Type': 'application/json'}
    r = session.post(url='https://jwgls1.cust.edu.cn/api/LoginApi/LGSSOLocalLogin?sf_request_type=ajax',
                            data=json.dumps(asp_net_sessionid_param), headers=headers)
    data = json.loads(r.content.decode('utf-8'))
    # print(data)
    # 提示未建立教务信息
    # if data['state'] == 1:
    #     return (data['message'], 513)
    # student_name = data['data']['StudentDto']['XM']
    # self.__student_id = data['data']['StudentDto']['XH']
    # return ('ok', 200)
    datepost = {
        "param": "JTdCJTdE", "__permission": {"MenuID": "00000000-0000-0000-0000-000000000000", "Operation": 0},
        "__log": {"MenuID": "00000000-0000-0000-0000-000000000000", "Logtype": 6, "Context": "\u67E5\u8BE2"}

    }
    r = session.post(url='https://jwgls1.cust.edu.cn/api/ClientStudent/Home/StudentHomeApi/QueryStudentScheduleData',
                     data=json.dumps(datepost), headers=headers)
    data = json.loads(r.content.decode('utf-8'))
    return data

def dodata(data):
    dataall = []
    data = data.get('data')
    data = data.get('AdjustDays')
    # print(data[0])
    for i in range(0,len(data)):
        data0 = data[i]['AM__TimePieces']
        for j in range(0,len(data0)):
            dataall.append(data0[j])
        data1 = data[i]['PM__TimePieces']
        for e in range(0,len(data1)):
            dataall.append(data1[e])
        data2 = data[i]['EV__TimePieces']
        for f in range(0, len(data2)):
            dataall.append(data2[f])
    datamain0 = []
    for h in range(0,len(dataall)):
        datamain0.append(dataall[h].get('Dtos'))
    datamain = []
    for i in range(0,len(datamain0)):
        if len(datamain0[i]) == 0:
            datamain.append('')
        elif len(datamain0[i]) == 1:
            if len(datamain0[i][0]['Content']) ==3:
                datamain.append(datamain0[i][0]['Content'][0]['Name']+ ";"+datamain0[i][0]['Content'][1]['Name']+ ";"+datamain0[i][0]['Content'][2]['Name'])
            else:
                datamain.append(datamain0[i][0]['Content'][0]['Name'] + ";"+ datamain0[i][0]['Content'][1]['Name'] + ";"+
                                datamain0[i][0]['Content'][2]['Name']+ ";"+datamain0[i][0]['Content'][3]['Name'])
        elif len(datamain0[i]) >= 1:
            a = ''
            for m in range(0,len(datamain0[i])):

                if len(datamain0[i][m]['Content']) == 3:
                    a = a + "".join(
                        datamain0[i][m]['Content'][0]['Name'] + ";" + datamain0[i][m]['Content'][1]['Name'] + ";" +
                        datamain0[i][m]['Content'][2]['Name'] + ";")

                else:
                    a = a + "".join(
                        datamain0[i][m]['Content'][0]['Name'] + ";" + datamain0[i][m]['Content'][1]['Name'] + ";" +
                        datamain0[i][m]['Content'][2]['Name'] +";"+ datamain0[i][m]['Content'][3]['Name'] +";" )
            datamain.append(a)
    print(datamain)
    print(len(datamain))
    return datamain

def savadata(datam):
    print(datam[0])

    # 测试连接成功与否
    try:
        db = pymysql.connect(
            host='zhangst333.mysql.rds.aliyuncs.com',
            port= 3307,
            user='zhangst',
            password='Root_test',
            database='sys'

        )

        print('数据库连接成功!')
    except pymysql.Error as e:
        print('数据库连接失败'+str(e))
    db = pymysql.connect(
        host='zhangst333.mysql.rds.aliyuncs.com',
        user='zhangst',
        port=3307,
        password='Root_test',
        database='sys'
    )
    cur = db.cursor()

    cur.execute('DROP TABLE IF EXISTS ZDD1')

    # 编辑sql 语句
    sqlQuery = '''CREATE  TABLE ZDD1(
              id  int PRIMARY KEY AUTO_INCREMENT,
              am1 varchar (255),
              am2 varchar (255),
              pm1 varchar (255),
              pm2 varchar (255),
              ev1 varchar (255),
              ev2 varchar (255)
              )

    '''
    cur.execute(sqlQuery)
    db.commit()

    sqlQuerypost1 = '''
     insert into ZDD1 (
     am1,am2,pm1,pm2,ev1,ev2) values (%s,%s,%s,%s,%s,%s)
    
    '''
    for i in range(0,7):
        values = (datam[i*6+0], datam[i*6+1], datam[i*6+2], datam[i*6+3], datam[i*6+4], datam[i*6+5])
        cur.execute(sqlQuerypost1, values)
        db.commit()
    db.close()
    print("数据储存成功!")
if __name__ == '__main__':
    print("请输入用户名:（入学年份为开头 例：2019001097）")
    username =input()
    print("请输入密码:")
    password =input()
    data = dataget(username,password)
    data = dodata(data)
    savadata(data)














