"""This module contains class FlightSearcher"""


class ClassFlightsSearcher:
    """This class implements flight search algorithm"""

    def __init__(self, context):
        self._context = context

    def searching(self):
        """This method searches flights"""

        if self._context.print_available_cities_flag:
            yield self._context.parameters_getter.available_cities_string

        self._set_correct_parameters()

        result_search_flights = self._context.airline_api. \
            searching_flights(*self._context.parameters,
                              self._context.flexible_dates_flag)

        yield self._context.handler.handle(result_search_flights)

    def _set_correct_parameters(self):
        """This method gets correct parameters"""

        while True:
            get_correct_parameters_result = self._context.parameters_getter. \
                get_correct_parameters(self._context.validator,
                                       self._context.parameters)

            if get_correct_parameters_result is not True:
                self._context.set_new_parameters(get_correct_parameters_result)
                continue

            confirm_search_parameters_result = self. \
                _context.parameters_getter.confirm_search_parameters(
                    self._context.parameters)

            if confirm_search_parameters_result is not True:
                self._context.set_new_parameters(
                    confirm_search_parameters_result)
                continue

            break
