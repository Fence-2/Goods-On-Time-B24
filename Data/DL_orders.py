import sys
import time

from Data.DL_api import Api
from Data.config import *
from tqdm import tqdm


def get_orders_info(orders, GS_session, SZ_session):
    with tqdm(total=len(orders), colour="blue", desc="Получение информации о заказах") as pbar:
        def get_orders_and_set_info(main_session, main_orders, reserve_orders):
            while len(main_orders) > 0:
                if len(main_orders) > 5:
                    info = main_session.get_orders_info_by_api(main_orders[:5])
                else:
                    info = main_session.get_orders_info_by_api(main_orders)

                for inf in info:
                    orderId = str(inf["orderId"])
                    if "error" in inf:
                        main_orders.remove(orderId)
                        pbar.update(1)
                        continue
                    if inf["sender"]["name"] is None:
                        reserve_orders.append(orderId)
                    else:
                        pbar.update(1)
                        order = orders[orderId]
                        order.percent_progress = str(inf["progressPercent"]) + "%"
                        order.status = inf["stateName"]
                        order.dest_company = inf["receiver"]["name"]
                        order.apr_arrival_date = inf["orderDates"]["arrivalToReceiver"]
                        order.dest_city = inf["arrival"]["city"]
                        order.price = str(inf["totalSum"])

                    main_orders.remove(orderId)
            return main_orders, reserve_orders

        simple_orders = [(k, v.B24_order) for k, v in orders.items()]
        GS_orders, SZ_orders = list(), list()
        for order in simple_orders:
            if order[1].startswith("СЗ"):
                SZ_orders.append(order[0])
            else:
                GS_orders.append(order[0])

        GS_orders, SZ_orders = get_orders_and_set_info(GS_session, GS_orders, SZ_orders)
        SZ_orders, GS_orders = get_orders_and_set_info(SZ_session, SZ_orders, GS_orders)
        GS_orders, SZ_orders = get_orders_and_set_info(GS_session, GS_orders, SZ_orders)
    sys.stdout.flush()
    time.sleep(0.5)

if __name__ == "__main__":
    GS_session = Api(tokens[0], users[0][0], users[0][1])
    SZ_session = Api(tokens[0], users[1][0], users[1][1])
    #  [print(f"{v.B24_order}: {k}") for k, v in orders.items()]
    get_orders_info(orders, GS_session, SZ_session)

    for k, v in orders.items():
        print(v)

    GS_session.disconnect()
    SZ_session.disconnect()
