from Data.config import *
import Data.DL_orders as DL
from prettytable import PrettyTable
import os
from Data.DL_api import Api


def convert_to_table(additional_fields):
    result = list()
    k = 0
    for i, track in enumerate(orders):
        result.append(list())
        result[i - k].append(str(track))
        result[i - k].append(orders[track].B24_order)
        percent = orders[track].percent_progress
        percent = percent if percent not in ["None", None, "None%"] else "Неизв"
        result[i - k].append(percent)
        if "Статус" in additional_fields:
            result[i - k].append(orders[track].status)
        if "Компания получатель" in additional_fields:
            result[i - k].append(orders[track].dest_company)
        if "Город назначения" in additional_fields:
            result[i - k].append(orders[track].dest_city)
        result[i - k].append(orders[track].price)
        result[i - k].append(orders[track].is_paid)
    result_unknown = sorted(list(filter(lambda x: x[2] == "Неизв", result)), key=lambda y: y[1])
    result_100 = sorted(list(filter(lambda x: x[2] != "Неизв" and int(x[2][:-1]) == 100, result)), key=lambda y: y[1])
    result_not_100 = sorted(list(filter(lambda x: x[2] != "Неизв" and int(x[2][:-1]) != 100, result)), key=lambda y: int(y[2][:-1]), reverse=True)

    return result_100 + result_not_100 + result_unknown


def launch_scan(additional_fields=None):
    if additional_fields is None:
        additional_fields = ["Статус", "Компания получатель"]
    GS_session = Api(tokens[0], users[0][0], users[0][1])
    SZ_session = Api(tokens[0], users[1][0], users[1][1])

    DL.get_orders_info(orders, GS_session, SZ_session)
    try:
        orders_table = PrettyTable()
        orders_table.field_names = ["Трек-номер", "Заказ B24", "Прогресс",] + additional_fields + ["Стоимость доставки", "Оплата",]
        orders_table.add_rows(convert_to_table(additional_fields))
        print(orders_table)
    except Exception as e:
        print(e)
        return 1
    finally:
        GS_session.disconnect()
        SZ_session.disconnect()

        print()
        counteragents = DL.get_balances()
        counteragents_table = PrettyTable()
        counteragents_table.field_names = ["Юр. лицо", "Баланс после оплаты", "Дата баланса"]
        for agent in counteragents:
            counteragents_table.add_row([agent['name'], agent['balance'], agent['balance_date']])
        print(counteragents_table)


def init():
    update_orders_with_B24_number()
    print(
        "Добро пожаловать в Менеджер заказов ТК!\n"
        "Стандартные параметры:\n"
        "-Выводится только: трек-номер, заказ Б24, прогресс, статус, компания\n\n"
        "Продолжить без изменений? (y/n)")
    choise = input().lower()

    if choise in ("y", "yes", "д", "да", "", "\n"):
        launch_scan()
    elif choise in ("n", "no", "н", "нет"):
        print("1. Статус заказа (комментарий от ТК)\n"
              "2. Компания получатель\n"
              "3. Город назначения\n"
              "4. Стоимость доставки\n\n"
              "Введите слитно номера полей, которые должны будут отображаться в таблице:")
        fields_nums = set(input())
        fields = list()
        if "1" in fields_nums: fields.append("Статус")
        if "2" in fields_nums: fields.append("Компания получатель")
        if "3" in fields_nums: fields.append("Город назначения")
        if "4" in fields_nums: fields.append("Стоимость доставки")

        launch_scan(fields)

    else:
        print("Я вас не понял, давайте попробуем снова.\n")
        init()


if __name__ == '__main__':
    init()
    os.system("pause")
