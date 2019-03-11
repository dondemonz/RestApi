import requests
from model.check_event_gate_response import check_event_gate_response
from model.json_check import *
from model.input_data import *
import time

# Создание и получение подписки
def test_GetV1SubscriptionByIdCode200And401AndPostV1SubscriptionCode201AndSendPostCallback(fix):
    data = {"callback": "http://localhost:88/event?", "filter": {"action": "EVENT", "id": "777", "type": "TEST"}}
    post_response = requests.post(url="http://" + slave_ip + ":8888/api/v1/events/subscriptions", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "201"
    assert str(post_response.status_code) == user_resp_code
    body = json.dumps(post_response.json())
    data1 = json.loads(body)
    subscription_id = data1["data"]["id"]

    fix.connect_to_dll()
    fix.send_event(message="TEST|777|EVENT".encode("utf-8"))
    time.sleep(3)
    # print(fix.cb1)


    action, id, method, path, peer_address, type = check_event_gate_response(fix)
    assert action == "EVENT" and id == "777" and type == "TEST" and method == "POST" and path == "event" and peer_address == "::1"

    response = requests.get(url="http://" + slave_ip + ":8888/api/v1/events/subscriptions/"+subscription_id, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data2 = json.loads(body)
    subscription_id1 = data2["data"]["id"]
    assert subscription_id == subscription_id1

    response1 = requests.get(url="http://" + slave_ip + ":8888/api/v1/events/subscriptions/" + subscription_id, auth=("", ""))
    user_resp_code = "401"
    assert str(response1.status_code) == user_resp_code

def test_PostV1SubscriptionCode401():
    response = requests.post(url="http://" + slave_ip + ":8888/api/v1/events/subscriptions", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_GetV1SubscriptionsByIdCode404():
    data = "Unknown Task id:0"
    response = requests.get(url="http://" + slave_ip + ":8888/api/v1/events/subscriptions/0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_GetV1SubscriptionsCode200():
    data = "success"
    response = requests.get(url="http://" + slave_ip + ":8888/api/v1/events/subscriptions/", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n

def test_GetV1SubscriptionsCode401():
    response = requests.get(url="http://" + slave_ip + ":8888/api/v1/events/subscriptions/", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code
