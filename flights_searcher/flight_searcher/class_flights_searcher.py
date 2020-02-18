import sys
from requests import exceptions as request_exceptions
from interfaces.interface_flights_searcher import InterfaceFlightsSearcher


class ClassFlightsSearcher(InterfaceFlightsSearcher):
    """This class implements flight search algorithm"""

    def searching(self):
        """
        This method validates input parameters, searches flights and
        handles search result

        This method return generator of available cities string (if
        print_available_cities_flag is True) and result search flights string
        As well as, this method handles exceptions
        """

        try:
            available_cities = self._context.\
                airline_api.get_available_cities()
            if self._context.print_available_cities_flag:
                yield self._context.validator.create_available_cities_string(
                    available_cities)
            try:
                parameters = self._context.validator.get_correct_parameters(
                    self._context.parameters, available_cities)

            except KeyboardInterrupt:
                print('Good buy. Thanks for using our app')
                sys.exit(0)

            result_search_flights = self._context.airline_api.\
                searching_flights(*parameters,
                                  self._context.flexible_dates_flag)

        except request_exceptions.HTTPError as error:
            print(error, 'Please try again later')
            sys.exit(1)

        except request_exceptions.RequestException:
            print('Cannot get response from airline. '
                  'Please check your internet connection '
                  'and restart the application')
            sys.exit(1)

        try:
            yield self._context.handler.handle(result_search_flights)

        except IndexError:
            print('Failed to find all the necessary '
                  'information in the response from '
                  'airline. Please try searching again.')
            sys.exit(1)
