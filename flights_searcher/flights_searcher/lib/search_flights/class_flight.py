class Flight:
    def __init__(self, flight_dict):
        if not all(flight_dict.values()):
            raise KeyError

        self.departure_city = flight_dict['from']
        self.arrival_city = flight_dict['to']
        self.flight = flight_dict['flight']
        self.route = flight_dict['route']
        self.departure_time = flight_dict['depart']
        self.arrival_time = flight_dict['arrive']
        self.flight_duration = self.arrival_time - self.departure_time
        self.flight_class = flight_dict['class']
        self.price = flight_dict['price']
        self.currency = flight_dict['currency']

    def sum_price(self, other):
        sum_price_dict = {self.currency: self.price}

        sum_price_dict[other.currency] = (
            sum_price_dict.setdefault(other.currency, 0) + other.price)

        sum_price_string = ''
        for key, value in sum_price_dict.items():
            sum_price_string += str(value) + ' ' + key + '\n'

        return sum_price_string

    def __str__(self):
        string = ''
        for key, value in self.__dict__.items():
            string += f'{key.replace("_", " ")} : {value}\n'

        return string
