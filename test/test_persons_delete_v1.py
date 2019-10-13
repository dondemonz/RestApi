import requests
from model.json_check import *
from model.input_data import *
import time

def test_DeleteV1PersonsCode200(fix):
    data = {"status": "success"}
    fix.send_event(message=(("CORE||CREATE_OBJECT|objtype<PERSON>,objid<1.888>,parent_id<1.999>,name<Test_Person_For_Delete>").encode("utf-8")))
    time.sleep(3)
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/1.888", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    assert data == data1

def test_DeleteV1PersonsCode401():
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/999.0", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_DeleteV1PersonsCode404():
    data = "Person 0 not found."
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n