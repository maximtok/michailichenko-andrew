import sys
import click
from search_flights.search_flights import search_flights
from search_flights.print_flights import print_flights
from exceptions.flights_searcher_exceptions import FlightsSearcherError

@click.command(context_settings=dict(allow_extra_args=True))
@click.pass_context
def main(search_parameters):
    """This application can search flights\n
    Example input parameters: KHI ISB 02.02.2020 05.02.2020\n
    IATA-code must be three capital letters\n
    Date must be a format DD.MM.YYYY\n"""

    search_parameters = search_parameters.args
    if len(search_parameters) == 0:
        search_parameters = input(
            'Enter the search parameters with a space\n').split()
    while True:
        try:
            flights = search_flights(search_parameters)
        except (EOFError, KeyboardInterrupt):
            print('Good buy. Thanks for using our app')
            break

        except FlightsSearcherError as error:
            print(error)

            sys.exit(1)

        print_flights(flights)

        try:
            if input('Search again? (y/n)\n') == 'y':

                search_parameters = input(
                    'Enter the search parameters with a space\n').split()
            else:
                print('Good buy. Thanks for using our app')
                break

        except (EOFError, KeyboardInterrupt):
            print('Good buy. Thanks for using our app')
            break

    sys.exit(0)


if __name__ == '__main__':
    main()
