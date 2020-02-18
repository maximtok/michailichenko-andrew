from copy import deepcopy


class Flight:
    """This class implements flight"""

    def __init__(self, **kwargs):
        self.departure_city = kwargs['from']
        self.arrival_city = kwargs['to']
        self.flight = kwargs['flight']
        self.route = kwargs['route']
        self.departure_time = kwargs['depart']
        self.arrival_time = kwargs['arrive']
        self.flight_duration = self.arrival_time - self.departure_time
        self.flight_class = kwargs['class']
        self.price = kwargs['price']
        self.currency = kwargs['currency']
        self.displayed_attributes_dict = deepcopy(self.__dict__)

    def create_total_price_string(self, other):
        """This method create total price string two flights"""

        sum_price_dict = {self.currency: self.price}

        sum_price_dict[other.currency] = (
            sum_price_dict.setdefault(other.currency, 0) + other.price)

        result_string = '\n'.join([f'{value}: {key}'
                                   for value, key
                                   in sum_price_dict.items()])

        return result_string + '\n'

    def __str__(self):
        result_string = '\n'.join([f'{attribute_name}: {attribute_value}'
                                   for attribute_name, attribute_value
                                   in self.displayed_attributes_dict.items()])

        return result_string + '\n'
