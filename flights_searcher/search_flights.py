"""This module contains searching_flights function"""

import sys
from requests import exceptions as request_exceptions
from class_global_context import GlobalContext
from flight_searcher.class_flights_searcher import ClassFlightsSearcher
from repeat_search_decorator import repeat_search_decorator


@repeat_search_decorator
def searching_flights(search_parameters, **kwargs):
    """This function searches flights"""

    try:
        context = GlobalContext(search_parameters, **kwargs)
        result = ClassFlightsSearcher(context).searching()

        for string in result:
            print(string)

    except request_exceptions.HTTPError as error:
        print(error, 'Please try again later')
        sys.exit(1)

    except request_exceptions.RequestException:
        print('Cannot get response from airline. '
              'Please check your internet connection '
              'and restart the application')
        sys.exit(1)

    except IndexError:
        print('Failed to find all the necessary '
              'information in the response from '
              'airline. Please try searching again.')
        sys.exit(1)

    except KeyboardInterrupt:
        print('Good buy. Thanks for using our app')
        sys.exit(0)
