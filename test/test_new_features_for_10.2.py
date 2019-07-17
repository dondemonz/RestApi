import requests
from model.json_check import *
from model.input_data import *
import time

def test_ApiV1DepartmentsCode200(fix):
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<DEPARTMENT>,objid<8>,parent_id<1>,name<Test_Department8>").encode("utf-8"))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<PERSON>,objid<1.999>,parent_id<8>,name<" + user + ">,passwd<" + password + ">").encode("utf-8"))
    data = {"status": "success"}
    fix.send_event(message=(("CORE||CREATE_OBJECT|objtype<PERSON>,objid<1.888>,parent_id<1.999>,name<Test_Person_For_Delet>").encode("utf-8")))
    time.sleep(3)
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/1.888", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    assert data == data1



    #{"data": [{"id": "1.1", "name": "Department 1"}, {"id": "1.2", "name": "Department 2"}],
     #"status": "success"}

def test_123(fix):
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<DEPARTMENT>,objid<8>,parent_id<1>,name<Test_Department8>").encode("utf-8"))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<PERSON>,objid<1.999>,parent_id<8>,name<" + user + ">,passwd<" + password + ">").encode("utf-8"))