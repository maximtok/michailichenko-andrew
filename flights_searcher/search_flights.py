from class_global_context import GlobalContext
from flight_searcher.class_flights_searcher import ClassFlightsSearcher
from repeat_search_decorator import repeat_search_decorator


@repeat_search_decorator
def searching_flights(search_parameters, **kwargs):
    """This function searches flights"""
    context = GlobalContext(search_parameters, **kwargs)

    result = ClassFlightsSearcher(context).searching()
    for string in result:
        print(string)
