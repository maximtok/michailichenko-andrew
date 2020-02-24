"""This module contains class Handler"""

from itertools import product
from interfaces.interface_handler import InterfaceHandler
from handlers.class_flight import Flight


class Handler(InterfaceHandler):
    """This class implements search flights result dictionary handler"""

    def handle(self, dict_result_search):
        """This method handles search flights result dictionary"""

        list_result_search = [[Flight(**flight) for flight in trip]
                              for trip in
                              dict_result_search.values()]

        list_result_search = self._sorting_flights(list_result_search)

        if len(list_result_search) <= 1:

            return self._create_handled_search_flights_result_string(
                list_result_search)

        combinations = self._combine_flights(list_result_search)
        round_trips = self._round_trips_filtering(combinations)
        result = self._create_list_of_strings_with_total_price(round_trips)

        return self._create_handled_search_flights_result_string(result)

    @staticmethod
    def _sorting_flights(flights_info):
        """This method sorts flights for price"""

        for flights in flights_info:
            flights.sort(
                key=lambda flight: (flight.price, flight.currency))

        return flights_info

    @staticmethod
    def _combine_flights(flights_info):
        """This method combines flights and creates round trips"""

        return list(product(flights_info[0], flights_info[1]))

    @staticmethod
    def _round_trips_filtering(round_trips):
        """
        this method filters trips back there by removing those which
        direct flight arrival time > return flight departure time
        """

        result = filter(
            lambda round_trip: round_trip[1].departure_time > round_trip[
                0].arrival_time, round_trips)

        return result

    @staticmethod
    def _create_list_of_strings_with_total_price(round_trips):
        """This method creates list of strings with total price round trips"""

        return [[round_trip[0], round_trip[1],
                 'Total price: ' +
                 round_trip[0].create_total_price_string(round_trip[1])]
                for round_trip in round_trips]

    @staticmethod
    def _create_handled_search_flights_result_string(flights):
        """This method creates handled search flights result string"""

        if len(flights) == 0:

            return 'No flights found for your request'

        flights = [flight for round_trip in flights
                   for flight in round_trip]
        result_string = '\n'.join(map(str, flights))

        return 'Found flights:\n' + result_string
