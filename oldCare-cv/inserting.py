'''
将事件插入数据库主程序

用法：

'''

import json
import datetime
import time

import requests

def add_event(data):
    url = 'http://127.0.0.1:5000/addEvent'
    headers = {
            "applicationCode": "detection",
            "operationTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "Content-Type": "application/json;charset=UTF-8"
    }
    r=requests.post(url,headers=headers, json=data)
    r.encoding='utf-8'
    if r.status_code==200:
        print("11111")
        return True
    else:
        print(r)
        return False


#eventtype:1:老人笑；2：摔倒；3：陌生人出现；4：禁区闯入；5：义工和老人交互
def insert(event_type,event_location,event_desc,image_base,path=None,old_people_id=None,volunteer_id=None):
    global backendws,frontendws

    f = open('allowinsertdatabase.txt','r')
    content = f.read()
    f.close()
    allow = content[11:12]
    print("allow:"+allow)

    if allow == '1': # 如果允许插入

        f = open('allowinsertdatabase.txt','w')
        f.write('is_allowed=1')
        f.close()

        print('准备插入数据库')

        event_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        mes = {'eventDesc':event_desc,
               'eventType':event_type,
               'eventDate':event_date,
               'eventLocation':event_location,
               'oldpersonId':old_people_id,
               'volunteerId':volunteer_id,
               'eventImageDir':path,
               # 'image':image_base
               }

        print(mes)

        add_event(mes)
        # r=redisinit.get_connection()
        # r.set('event',json.dumps(mes))
        # print(r.get('event'))
        print('插入成功')
    else:
        print('just pass')
