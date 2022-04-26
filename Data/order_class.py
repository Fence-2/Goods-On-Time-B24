class Order:
    def __init__(self, track,
                 B24_order="Неизвестный Б24 заказ",
                 percent_progress="-1%",
                 status="None",
                 apr_arrival_date="None",
                 dest_company="None",
                 dest_city="None",
                 price="None",
                 is_paid="None"):
        self.track = track
        self.B24_order = B24_order
        self.percent_progress = percent_progress
        self.status = status
        self.apr_arrival_date = apr_arrival_date
        self.dest_company = dest_company
        self.dest_city = dest_city
        self.price = price
        self.is_paid = is_paid

    def __str__(self):
        all_ = [i for i in [self.B24_order, self.percent_progress, self.status, self.apr_arrival_date,
                         self.dest_company, self.dest_city, self.price, self.is_paid] if i not in ["-1%", "None"]]
        all_ = [str(i) for i in all_]
        result = str(self.track) + "\n\t" + str('\n\t'.join(all_))

        return result
