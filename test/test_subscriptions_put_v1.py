import requests
from model.check_event_gate_response import check_event_gate_response
from model.json_check import *
from model.input_data import *
import time
from parse import *

# Изменение подписки
def test_PutV1SubscriptionsCode200And401AndSendPostCallback(fix):
    data = {"callback": "http://localhost:88/event?", "filter": {"action": "EVENT", "id": "", "type": "TEST"}}
    response = requests.post(url="http://" + slave_ip + ":8888/api/v1/events/subscriptions", headers=headers, data=json.dumps(dict(data)), auth=auth)
    body = json.dumps(response.json())
    data1 = json.loads(body)
    subscription_id = data1["data"]["id"]
    #print("1---"+subscriptionId)

    data1 = {"callback": "http://localhost:88/event?", "filter": {"action": "ACTION", "id": "555", "type": "OBJECT"}}
    response = requests.put(url="http://" + slave_ip + ":8888/api/v1/events/subscriptions/"+subscription_id, headers=headers, data=json.dumps(dict(data1)), auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    subscription_id1 = data1["data"]["id"]
    assert subscription_id == subscription_id1

    fix.connect_to_dll()
    fix.send_event(message="OBJECT|555|ACTION".encode("utf-8"))
    time.sleep(3)
    # print(fix.cb1)

    action, id, method, path, peer_address, type = check_event_gate_response(fix)
    assert action == "ACTION" and id == "555" and type == "OBJECT" and method == "POST" and path == "event" and peer_address == "::1"

    response1 = requests.put(url="http://" + slave_ip + ":8888/api/v1/events/subscriptions/" + subscription_id, auth=("", ""))
    user_resp_code = "401"
    assert str(response1.status_code) == user_resp_code


def test_PutV1SubscriptionsCode404():
    data1 = {"callback": "http://localhost:9786/event?", "filter": {"action": "ACTION", "id": "555", "type": "OBJECT"}}
    data = "Unknown Subscription id:0"
    response = requests.put(url="http://" + slave_ip + ":8888/api/v1/events/subscriptions/0", headers=headers, data=json.dumps(dict(data1)), auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n
