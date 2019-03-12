import requests
from model.json_check import *
from model.input_data import *
import time
import datetime as dt
import winreg
import psutil


def test_create_key_and_pareams():   # создает параемтры в реестре
    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\ISS\\SecurOS\\Niss400\\ImageProcessor")
    winreg.SetValueEx(key, 'deltaArchive', 0, winreg.REG_SZ, '1')
    winreg.SetValueEx(key, 'downloadTimeout', 0, winreg.REG_SZ, '2')

# срубает image_export.exe для того, чтобы применились параметры реестра. !!!работает только если pycharm запущен от администратора!!!
def test_reload_video_exe():
    PROCNAME = "image_export.exe"
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()
    time.sleep(5)

def test_GetV2CameraProtocolCode200(fix):
    data = 2
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")  # почему иногда использовал "%Y-%m-%d %H:%M:%S" - почему - непонятно
    fix.connect_to_dll()
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    p = dt.datetime.now()
    endtime = (p.strftime("%Y%m%dT%H%M%S"))
    time.sleep(3)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime + "&stop_time=" + endtime + "&max_count=3", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n



def test_GetV2CameraProtocolCode200WithoutEndTime(fix):
    data = 1
    m = dt.datetime.now()
    # print(m)
    # print(m.strftime("%Y-%m-%d %H:%M:%S"))
    # v = m.time()
    # print(v)
    starttime = m.strftime("%Y%m%dT%H%M%S")
    fix.connect_to_dll()
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime + "&max_count=1", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n


def test_GetV2CameraProtocolCode200WithoutEndTimeAndMaxCount(fix):
    data = 2
    m = dt.datetime.now()
    # print(m)
    # print(m.strftime("%Y-%m-%d %H:%M:%S"))
    # v = m.time()
    # print(v)
    starttime = m.strftime("%Y%m%dT%H%M%S")
    fix.connect_to_dll()
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n


def test_GetV2CameraProtocolCode400():
    data = "Missed required parameter:start_time"
    response = requests.get(url="http://"+slave_ip+":8888/api/v1/cameras/"+camId+"/protocol", auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_GetV2CameraProtocolCode400IncorrectTime(fix):
    data = "Incorrect parameter:start_time, value:20151119T1848032"
    response = requests.get(url="http://"+slave_ip+":8888/api/v1/cameras/"+camId+"/protocol?start_time=20151119T1848032", auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_GetV2CameraProtocolCode401(fix):
    data = {"name": camName}
    fix.connect_to_dll()
    response = requests.put(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"", headers=headers, data=json.dumps(dict(data)), auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

# Тесты фильтров для протокола
def test_GetV2CameraProtocolCode200EventFilterEmpty(fix):
    data = 0
    fix.connect_to_dll()
    fix.send_event(message=("CORE||UPDATE_OBJECT|objtype<REST_API>,objid<" + objId + ">,parent_id<" + slave + ">,event_filter_id<"+objId+">").encode("utf-8"))
    fix.send_event(message=("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<0>,EVENT.type.count<0>,EVENT.id.count<0>,EVENT.rule.count<0>").encode("utf-8"))
    fix.disconnect()
    time.sleep(3)
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.connect_to_dll()
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n

def test_GetV2CameraProtocolCode200EventFilterAllowAll(fix):
    data = 2
    fix.connect_to_dll()
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<1>,EVENT.type.count<1>,EVENT.id.count<1>,EVENT.rule.count<1>,EVENT.rule.0<1>,EVENT.id.0<>,EVENT.type.0<CAM>,EVENT.action.0<>").encode("utf-8")))
    time.sleep(3)
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.callback_proto()
    fix.callback_wrapper()
    fix.connect()
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n

def test_GetV2CameraProtocolCode200EventFilterAllowId(fix):
    data = 2
    data2 = 0
    fix.connect_to_dll()
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<1>,EVENT.type.count<1>,EVENT.id.count<1>,EVENT.rule.count<1>,EVENT.rule.0<1>,EVENT.id.0<"+camId+">,EVENT.type.0<CAM>,EVENT.action.0<>").encode("utf-8")))
    time.sleep(3)
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n
    response1 = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId1+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    assert data2 == n2


def test_GetV2CameraProtocolCode200EventFilterAllowEvent(fix):
    data = 1
    data2 = 1
    fix.connect_to_dll()
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<1>,EVENT.type.count<1>,EVENT.id.count<1>,EVENT.rule.count<1>,EVENT.rule.0<1>,EVENT.id.0<>,EVENT.type.0<CAM>,EVENT.action.0<ARMED>").encode("utf-8")))
    time.sleep(10)
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|DISARM").encode("utf-8"))
    time.sleep(2)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    time.sleep(10)
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    time.sleep(10)
    assert data == n

    response1 = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId1+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    time.sleep(10)
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    time.sleep(10)
    assert data2 == n2

def test_GetV2CameraProtocolCode200EventFilterAllowIdForbidAll(fix):
    data = 2
    data2 = 0
    fix.connect_to_dll()
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<2>,EVENT.type.count<2>,EVENT.id.count<2>,EVENT.rule.count<2>,EVENT.rule.0<1>,EVENT.id.0<"+camId+">,EVENT.type.0<CAM>,EVENT.action.0<>,EVENT.rule.1<0>,EVENT.id.1<>,EVENT.type.1<CAM>,EVENT.action.1<>").encode("utf-8")))
    time.sleep(3)
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n

    response1 = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId1+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    assert data2 == n2

def test_GetV2CameraProtocolCode200EventFilterAllowAllForbidId(fix):
    data = 0
    data2 = 2
    fix.connect_to_dll()
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<2>,EVENT.type.count<2>,EVENT.id.count<2>,EVENT.rule.count<2>,EVENT.rule.0<0>,EVENT.id.0<"+camId+">,EVENT.type.0<CAM>,EVENT.action.0<>,EVENT.rule.1<1>,EVENT.id.1<>,EVENT.type.1<CAM>,EVENT.action.1<>").encode("utf-8")))
    time.sleep(10)
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    time.sleep(10)
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    time.sleep(10)
    assert data == n

    response1 = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId1+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    time.sleep(10)
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    time.sleep(10)
    assert data2 == n2

def test_GetV2CameraProtocolCode200EventFilterAllowEventForbidAll(fix):
    data = 1
    data2 = 1
    fix.connect_to_dll()
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<2>,EVENT.type.count<2>,EVENT.id.count<2>,EVENT.rule.count<2>,EVENT.rule.0<1>,EVENT.id.0<>,EVENT.type.0<CAM>,EVENT.action.0<DISARMED>,EVENT.rule.1<0>,EVENT.id.1<>,EVENT.type.1<CAM>,EVENT.action.1<>").encode("utf-8")))
    time.sleep(3)
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n

    response1 = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId1+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    assert data2 == n2

def test_GetV2CameraProtocolCode200EventFilterAllowAllForbidEvent(fix):
    data = 1
    data2 = 1
    fix.connect_to_dll()
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<2>,EVENT.type.count<2>,EVENT.id.count<2>,EVENT.rule.count<2>,EVENT.rule.0<0>,EVENT.id.0<>,EVENT.type.0<CAM>,EVENT.action.0<DISARMED>,EVENT.rule.1<1>,EVENT.id.1<>,EVENT.type.1<CAM>,EVENT.action.1<>").encode("utf-8")))
    time.sleep(3)
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId1+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n

    response1 = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId1+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    assert data2 == n2
