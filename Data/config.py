import Data.logs
import os
from Data.order_class import Order

orders: dict[Order] = dict()
tokens, users = list(), list()

if not os.path.exists(r".\orders.txt"):
    with open(r".\orders.txt", "w", encoding="utf-8"):
        pass

if not os.path.exists(r".\config.txt"):
    with open(r".\config.txt", "w", encoding="utf-8") as file:
        file.writelines(["token=\n", "login=\n"])


def get_config():
    with open(r".\config.txt", encoding="utf-8") as config_file:
        for line in config_file:
            line = line.strip()
            if "=" in line:
                if line.startswith("token="):
                    tokens.append(line[6:])
                elif line.startswith("login=") and ":" in line:
                    users.append(tuple(line[6:].split(":")))


def update_orders_with_B24_number():
    with open(r".\orders.txt", encoding="utf-8") as orders_file:
        lines = orders_file.readlines()

    for line in lines:
        line = line.strip()
        if len(line) > 3 and not line.startswith("#"):
            B24_order, track = line.split(maxsplit=1)
            orders[track] = Order(track)
            orders[track].B24_order = B24_order


get_config()
update_orders_with_B24_number()
if not any(tokens):
    print("Для работы программы необходим токен Api Деловых Линий. "
          "Введите его в файл config.txt")
    os.system("pause")
    exit()
if not any(users):
    print("Для работы программы необходим логин и пароль аккаунта Деловых Линий.\n"
          "Введите его в файл config.txt")
    os.system("pause")
    exit()
