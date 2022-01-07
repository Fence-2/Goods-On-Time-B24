import time

import requests
from Data.config import tokens, users
import json
from Data.logs import log
from http.client import responses


class Api:
    sessionID: str

    def __init__(self, token: str, login: str, password: str):
        self.token = token
        self.login = login
        self.password = password

        self.connect()

    def connect(self):
        req = requests.post("https://api.dellin.ru/v3/auth/login.json", json={"appkey": self.token,
                                                                              "login": self.login,
                                                                              "password": self.password})
        #
        log(f"Создание новой сессии: {req.status_code}, {responses[req.status_code]}")
        if req.status_code == 200:
            self.sessionID = json.loads(req.text)["data"]["sessionID"]
            log(f"SessionID: {self.sessionID}")
            return True
        return False

    def disconnect(self):
        req = requests.post("https://api.dellin.ru/v3/auth/logout.json", json={"appkey": self.token,
                                                                               "sessionID": self.sessionID})
        #
        log(f"Закрытие сессии: {req.status_code}, {responses[req.status_code]}")
        if req.status_code == 200:
            log(f"Сессия успешно закрыта: {self.sessionID}")
        return json.loads(req.text)

    def get_orders_info_by_api(self, orders: list) -> list[dict]:
        if type(orders) in [str, int]:
            orders = [str(orders)]
        else:
            orders = [str(order) for order in orders]

        if len(orders) > 5:
            log(f"Ошибка! Попытка получения статуса больше 5-ти заказов за 1 запрос")
            return []

        req = requests.post("https://api.dellin.ru/v3/orders.json", json={"appkey": self.token,
                                                                          "sessionID": self.sessionID,
                                                                          "docIds": orders})
        #
        log(f"Получение информации о заказах: {req.status_code}, {responses[req.status_code]}")
        if req.status_code == 429:
            print("Слишком много запросов!")
            return []
        if req.status_code == 200:
            return json.loads(req.text)["orders"]
        elif len(orders) > 1:
            log("Запущен перебор заказов для поиска ошибки")
            new_orders = list()
            for order in orders:
                order_status: list = self.get_orders_info_by_api([order])
                if order_status is not False:
                    new_orders += order_status
            return new_orders
        elif req.status_code == 400:
            log("Ошибка: Неизвестный заказ: " + orders[0])
        return [{"error": 400, "orderId": orders[0]}]


if __name__ == '__main__':
    session = Api(tokens[0], users[0][0], users[0][1])

    my_orders = session.get_orders_info_by_api([25791591, 2334111111])
    print(len(my_orders))
    # print(my_orders)
    [print(f"{k}: {v}") for k, v in my_orders[0].items()]
    session.disconnect()
