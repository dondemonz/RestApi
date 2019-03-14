import requests
from model.json_check import *
from model.input_data import *
import time
import datetime as dt


#Отправка задачи на экспорт и запрос на получение информации по этой задаче
def test_GetV1TaskByIdCode200and401andPostV1Code201(fix):
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|REC").encode("utf-8"))
    time.sleep(4)
    fix.send_react(("CAM|"+camId+"|REC_STOP").encode("utf-8"))
    time.sleep(1)
    p = dt.datetime.now()
    endtime = p.strftime("%Y-%m-%d %H:%M:%S")
    # p = p.time()
    # print(p)
    data = {"camera": ""+camId+"", "from": starttime, "to": endtime}
    response = requests.post(url="http://" + slave_ip + ":8888/api/v1/export/tasks/", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "201"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    task_id = data1["data"]["id"]
    # print(task_id)

    data2 = "success"
    response1 = requests.get(url="http://" + slave_ip + ":8888/api/v1/export/tasks/"+task_id, auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    dataresp = json.loads(body1)
    assert data2 == dataresp["status"]

    response2 = requests.get(url="http://" + slave_ip + ":8888/api/v1/export/tasks/1" + task_id, auth=("", ""))
    user_resp_code = "401"
    assert str(response2.status_code) == user_resp_code

def test_PostV1TaskCode400(fix):
    data1 = "Appropriate ARCH_CNV is not available."
    fix.send_event(message=(("CORE|RANDOM|DISABLE_OBJECT|objtype<ARCH_CNV>,objid<"+objId+">,parent_id<"+slave+">").encode("utf-8")))
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|REC").encode("utf-8"))
    time.sleep(4)
    fix.send_react(("CAM|"+camId+"|REC_STOP").encode("utf-8"))
    time.sleep(1)
    p = dt.datetime.now()
    endtime = p.strftime("%Y-%m-%d %H:%M:%S")
    data = {"camera": ""+camId+"", "from": starttime, "to": endtime}
    response = requests.post(url="http://" + slave_ip + ":8888/api/v1/export/tasks/", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data2 = json.loads(body)
    n = data2["message"]
    assert data1 == n
    fix.send_event(message=(("CORE|RANDOM|ENABLE_OBJECT|objtype<ARCH_CNV>,objid<"+objId+">,parent_id<"+slave+">").encode("utf-8")))


def test_PostV1TaskCode404():
    data1 = "Camera 0 not found."
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(4)
    p = dt.datetime.now()
    endtime = p.strftime("%Y-%m-%d %H:%M:%S")
    data = {"camera": "0", "from": starttime, "to": endtime}
    response = requests.post(url="http://" + slave_ip + ":8888/api/v1/export/tasks/", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data2 = json.loads(body)
    n = data2["message"]
    assert data1 == n

# Отправка задачи на экспорт без логина/пароля
def test_PostV1TaskCode401(fix):
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|REC").encode("utf-8"))
    time.sleep(4)
    fix.send_react(("CAM|"+camId+"|REC_STOP").encode("utf-8"))
    time.sleep(1)
    p = dt.datetime.now()
    endtime = p.strftime("%Y-%m-%d %H:%M:%S")
    data = {"camera": ""+camId+"", "from": starttime, "to": endtime}
    response = requests.post(url="http://" + slave_ip + ":8888/api/v1/export/tasks/", headers=headers, data=json.dumps(dict(data)), auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

