import sys
import itertools
from datetime import timedelta
from requests import exceptions as request_exceptions
from validator_input_parameters.validation_search_parameters \
    import validation_search_parameters
from airblue_com_api.class_airblue_com_api import AirblueComApi
from search_flights.class_flight import Flight


def search_flights(parameters):
    try:
        parameters = validation_search_parameters(parameters)

        dict_result_search = AirblueComApi.search_flights(*parameters)
        list_result_search = [[Flight(flight) for flight in trip]
                              for trip in
                              dict_result_search.values()]

    except request_exceptions.HTTPError as error:
        print(error.__str__() + ' Please contact support')
        sys.exit(1)

    except request_exceptions.RequestException:
        print('Cannot get response from airblue.com. '
              'Please check your internet connection '
              'and restart the application')
        sys.exit(1)

    except (IndexError, KeyError):
        print('Failed to find all the necessary '
              'information in the response from '
              'airblue.com. Please try searching again '
              'or contact support.')
        sys.exit(1)

    except Exception:
        print('An error occurred while running '
              'the application. Please try searching '
              'again or contact support.')
        sys.exit(1)

    try:
        if len(list_result_search) == 1:
            result = sorted_flights(list_result_search)
        else:
            list_result_search = sorted_flights(list_result_search)
            combinations = combination_fligths(list_result_search)
            round_trips = round_trip_filtering(combinations)
            result = [[round_trip[0], round_trip[1],
                       'Total price: ' +
                       round_trip[0].sum_price(round_trip[1])]
                      for round_trip in round_trips]

    except Exception:
        print('An error occurred while running the '
              'application. Please try searching again '
              'or contact support.')

    return result


def sorted_flights(flights_info):
    for flights in flights_info:
        flights.sort(
            key=lambda flight: (flight.price, flight.currency))

    return flights_info


def combination_fligths(flights_info):
    if len(flights_info) == 2:
        result = list(itertools.product(flights_info[0], flights_info[1]))
    else:
        result = []

    return result


def round_trip_filtering(round_trips):
    result = filter(
        lambda round_trip: round_trip[1].departure_time - round_trip[
            0].arrival_time > timedelta(), round_trips)

    return result
