import requests
from model.json_check import *
from model.input_data import *
import time
import datetime as dt


def test_GetV2CameraProtocolCode200(fix):
    data = 2
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")  # почему иногда использовал "%Y-%m-%d %H:%M:%S", а иногда "%Y%m%dT%H%M%S" - непонятно
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    p = dt.datetime.now()
    endtime = (p.strftime("%Y%m%dT%H%M%S"))
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime + "&stop_time=" + endtime + "&max_count=3", auth=auth)
    user_resp_code = "200"
    time.sleep(3)
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
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime + "&max_count=1", auth=auth)
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
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n


def test_GetV2CameraProtocolCode400():
    data = "Missed required parameter:start_time"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId+"/protocol", auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_GetV2CameraProtocolCode400IncorrectTime():
    data = "Incorrect parameter:start_time, value:20151119T1848032"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId+"/protocol?start_time=20151119T1848032", auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_GetV2CameraProtocolCode401():
    data = {"name": camName}
    response = requests.put(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"", headers=headers, data=json.dumps(dict(data)), auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

# Тесты фильтров для протокола
def test_GetV2CameraProtocolCode200EventFilterEmpty(fix):
    data = 0
    fix.send_event(message=("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<0>,EVENT.type.count<0>,EVENT.id.count<0>,EVENT.rule.count<0>").encode("utf-8"))
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(1)
    fix.connect_to_dll()
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n

def test_GetV2CameraProtocolCode200EventFilterAllowAll(fix):
    data = 2
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<1>,EVENT.type.count<1>,EVENT.id.count<1>,EVENT.rule.count<1>,EVENT.rule.0<1>,EVENT.id.0<>,EVENT.type.0<CAM>,EVENT.action.0<>").encode("utf-8")))
    time.sleep(3)
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(1)
    fix.connect_to_dll()
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n

def test_GetV2CameraProtocolCode200EventFilterAllowId(fix):
    data = 2
    data2 = 0
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<1>,EVENT.type.count<1>,EVENT.id.count<1>,EVENT.rule.count<1>,EVENT.rule.0<1>,EVENT.id.0<"+camId+">,EVENT.type.0<CAM>,EVENT.action.0<>").encode("utf-8")))
    time.sleep(3)
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n
    response1 = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId2+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    assert data2 == n2


def test_GetV2CameraProtocolCode200EventFilterAllowEvent(fix):
    data = 1
    data2 = 1
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<1>,EVENT.type.count<1>,EVENT.id.count<1>,EVENT.rule.count<1>,EVENT.rule.0<1>,EVENT.id.0<>,EVENT.type.0<CAM>,EVENT.action.0<ARMED>").encode("utf-8")))
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n

    response1 = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId2+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    assert data2 == n2

def test_GetV2CameraProtocolCode200EventFilterAllowIdForbidAll(fix):
    data = 2
    data2 = 0
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<2>,EVENT.type.count<2>,EVENT.id.count<2>,EVENT.rule.count<2>,EVENT.rule.0<1>,EVENT.id.0<"+camId+">,EVENT.type.0<CAM>,EVENT.action.0<>,EVENT.rule.1<0>,EVENT.id.1<>,EVENT.type.1<CAM>,EVENT.action.1<>").encode("utf-8")))
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n

    response1 = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId2+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    assert data2 == n2

def test_GetV2CameraProtocolCode200EventFilterAllowAllForbidId(fix):
    data = 0
    data2 = 2
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<2>,EVENT.type.count<2>,EVENT.id.count<2>,EVENT.rule.count<2>,EVENT.rule.0<0>,EVENT.id.0<"+camId+">,EVENT.type.0<CAM>,EVENT.action.0<>,EVENT.rule.1<1>,EVENT.id.1<>,EVENT.type.1<CAM>,EVENT.action.1<>").encode("utf-8")))
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n

    response1 = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId2+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    assert data2 == n2

def test_GetV2CameraProtocolCode200EventFilterAllowEventForbidAll(fix):
    data = 1
    data2 = 1
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<2>,EVENT.type.count<2>,EVENT.id.count<2>,EVENT.rule.count<2>,EVENT.rule.0<1>,EVENT.id.0<>,EVENT.type.0<CAM>,EVENT.action.0<DISARMED>,EVENT.rule.1<0>,EVENT.id.1<>,EVENT.type.1<CAM>,EVENT.action.1<>").encode("utf-8")))
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    assert data == n

    response1 = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId2+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    assert data2 == n2

def test_GetV2CameraProtocolCode200EventFilterAllowAllForbidEvent(fix):
    data = 1
    data2 = 1
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,EVENT.action.count<2>,EVENT.type.count<2>,EVENT.id.count<2>,EVENT.rule.count<2>,EVENT.rule.0<0>,EVENT.id.0<>,EVENT.type.0<CAM>,EVENT.action.0<DISARMED>,EVENT.rule.1<1>,EVENT.id.1<>,EVENT.type.1<CAM>,EVENT.action.1<>").encode("utf-8")))
    time.sleep(1)
    m = dt.datetime.now()
    starttime = m.strftime("%Y-%m-%d %H:%M:%S")
    fix.send_react(("CAM|"+camId+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|ARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|DISARM").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId2+"|DISARM").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v2/cameras/"+camId+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["actual_count"]
    print(data1)
    assert data == n

    time.sleep(1)
    response1 = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId2+"/protocol?start_time=" + starttime, auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response1.json())
    data3 = json.loads(body1)
    n2 = data3["data"]["actual_count"]
    assert data2 == n2

    # после последнего теста выключаем фильтр из реста
    # fix.send_event(message=("CORE||UPDATE_OBJECT|objtype<REST_API>,objid<" + objId + ">,parent_id<" + slave + ">,event_filter_id<>").encode("utf-8"))
    # и обновить фильтр
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<" + objId + ">,parent_id<1>,EVENT.action.count<1>,EVENT.type.count<1>,EVENT.id.count<1>,EVENT.rule.count<1>,EVENT.rule.0<1>,EVENT.id.0<>,EVENT.type.0<>,EVENT.action.0<>").encode("utf-8")))


