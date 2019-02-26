import json


# возможно в будущем стоит подумать, как объединить с другими проверками, но пока так, из тестов я его убрал
def if_there_is_no_json(response):
    if response:
        print("Джисон есть")
    else:
        print("Джисона нет")
    print("Тест закончен")

# этот тест использовался везде для проверки есть ли вообще джисон, т.к. он приходит не везде, но затем проверку unknown заменил на полную проверку текста
def json_check(response):
    body = json.dumps(response.json())
    if "Unknown" in body or body is None:
        print("Джисон None или Unknown")
    else:
        print("Правильный джисон")
    print(body)
    print("Тест закончен")

# ранее использовал эту фунцию во всех тестах (response_code_check(response, user_resp_code)), сейчас заменил через assert
def response_code_check(response, user_resp_code):
    resp_code = str(response.status_code)
    # print(resp_code)
    if user_resp_code == resp_code:
        print("Response code: " + str(resp_code))
    else:
        print("!!! Wrong response code: " + str(resp_code) + " Expected: " + user_resp_code)



# джисон сконвертированный в строку и красиво показанный (в столбик)
# body = json.dumps(response.json(), indent=4)

# body1 = json.loads(response.content)
# print(body1['message'])
# message = body1['message']


# print(body1['message'])
# message = body1['message']

"""
# полный response
print(response)
# чистый джисон
print(response.json())
# тело распарсенного джисона
print(body)
"""