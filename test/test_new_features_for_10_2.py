import requests
from model.json_check import *
from model.input_data import *
import time

def test_CreateEnvironment(fix):
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<DEPARTMENT>,objid<8>,parent_id<1>,name<Test_Department8>").encode("utf-8"))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<PERSON>,objid<2.2>,parent_id<8>,name<2>,passwd2<2>").encode("utf-8"))
    # fix.send_event(message=("CORE||CREATE_OBJECT|objtype<REST_API>,objid<" + objId + ">,parent_id<" + slave + ">,name<Test_RestAPI>").encode("utf-8"))
    # fix.send_event(message=("CORE||UPDATE_OBJECT|objtype<REST_API>,objid<" + objId + ">,parent_id<" + slave + ">,event_filter_id<" + objId + ">,port<" + restPort + ">").encode("utf-8"))
    time.sleep(1)


def test_ApiV1DepartmentsCode200():
    data = "success"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/departments", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n
    id = data1["data"][1]["id"]
    assert id == "8"

def test_ApiV1DepartmentsIdCode200(fix):
    data = "success"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/departments/8", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n
    id = data1["data"]["id"]
    assert id == "8"


def test_ApiV1DepartmentsIdCode404(fix):
    data = "Unknown DEPARTMENT id:0"
    response = requests.get(url="http://" + slave_ip + ":" + restPort + "/api/v1/departments/0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_ApiV1UserRightsCode200(fix):
    data = "success"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/user_rights", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n
    id = data1["data"][0]["name"]
    assert id == "Права опытных пользователей"

def test_ApiV1UserRightsIdCode200(fix):
    data = "success"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/user_rights/1.2", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n
    id = data1["data"]["id"]
    assert id == "1.2"


def test_ApiV1UserRightsIdCode404(fix):
    data = "Unknown RIGHTS id:0"
    response = requests.get(url="http://" + slave_ip + ":" + restPort + "/api/v1/user_rights/0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_PutV1PersonsCode200():
    data = {"user_rights_id": "1.1", "passwd": "3"}
    response = requests.put(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/2.2", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["name"]
    assert n == "2"

def test_PutV1PersonsCode404(fix):
    data = {"user_rights_id": "1.1", "passwd": "3"}
    data2 = "Person 0 not found."
    response = requests.put(url="http://" + slave_ip + ":" + restPort + "/api/v1/persons/0", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data2 == n

def test_PutV1PersonsCode304():
    data = {"user_rights_id": "9.9", "passwd": "3"}
    response = requests.put(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/2.2", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "304"
    assert str(response.status_code) == user_resp_code
    # тут должно приходить сообщение json: { "status":"fail", "message":"User rights 1.1 doesn't exist"});, но разработчики специально сделали, что его
    # увидеть можно только через wireshark

def test_PutV1PersonsCode403(fix):
    #fix.send_event(message="CORE||UPDATE_OBJECT|objtype<RIGHTS>,objid<1.1>,PERSON.person.count<1>,PERSON.person.0<1.11>".encode("utf-8"))
    data = {"user_rights_id": "1.1", "passwd": "3"}
    response = requests.put(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/2.2", headers=headers, data=json.dumps(dict(data)), auth=("2", "3"))
    user_resp_code = "403"
    assert str(response.status_code) == user_resp_code


def test_PutV1PersonsCode400(fix):
    data = {"name": "1"}
    data2 = "User 1 already exists"
    response = requests.put(url="http://" + slave_ip + ":" + restPort + "/api/v1/persons/2.2", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data2 == n

def test_PutV1PersonsCode403v2(fix):
    data = {"name": "3"}
    response = requests.put(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/2.2", headers=headers, data=json.dumps(dict(data)), auth=("2", "3"))
    user_resp_code = "403"
    assert str(response.status_code) == user_resp_code


def test_PostV1PersonsCode201():
    data = {"department_id": "1.1", "name": "5", "user_rights_id": "1.1"}
    response = requests.post(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "201"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["name"]
    assert n == "5"


def test_PostV1PersonsCode400v1():
    data = {"department_id": "1.1", "name": "6", "user_rights_id": "1.99"}
    data2 = "User rights 1.99 doesn't exist"
    response = requests.post(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data2 == n

def test_PostV1PersonsCode400v2():
    data = {"department_id": "1.99", "name": "5", "user_rights_id" : "1.1"}
    data2 = "Department 1.99 doesn't exist"
    response = requests.post(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data2 == n

def test_PostV1PersonsCode400v3():
    data = {"department_id": "1.1", "name": "5", "user_rights_id" : "1.1"}
    data2 = "User 5 already exists"
    response = requests.post(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data2 == n

def test_PostV1PersonsCode403v1():
    data = {"department_id": "1.1", "name": "6", "user_rights_id": "1.1"}
    response = requests.post(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons", headers=headers, data=json.dumps(dict(data)), auth=("2", "3"))
    user_resp_code = "403"
    assert str(response.status_code) == user_resp_code


def test_PostV1PersonsCode403v2():
    data = {"department_id": "1.1", "name": "5", "user_rights_id": "1.1"}
    response = requests.post(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons", headers=headers, data=json.dumps(dict(data)), auth=("2", "3"))
    user_resp_code = "403"
    assert str(response.status_code) == user_resp_code

def test_PostV1PersonsCode400v4():
    data = {"name": "", "user_rights_id": "1.1"}
    data2 = "name is not specified"
    response = requests.post(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data2 == n



def test_DeleteV1PersonsCode200():
    response = requests.delete(url="http://" + slave_ip + ":" + restPort + "/api/v1/persons/1000", headers=headers,  auth=auth)
    data = "success"
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert n == data

def test_DeleteV1PersonsCode403():
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/2.2", headers=headers, auth=("2", "3"))
    user_resp_code = "403"
    assert str(response.status_code) == user_resp_code

def test_DeleteEnvironment(fix):
    fix.send_event(message="CORE||DELETE_OBJECT|objtype<DEPARTMENT>,objid<8>".encode("utf-8"))





