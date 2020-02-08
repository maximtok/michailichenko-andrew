import sys
import click
from search_flights.search_flights import search_flights
from search_flights import print_flights
from airblue_com_api.class_airblue_com_api \
    import AirblueComApi

@click.command(context_settings=dict(allow_extra_args=True))
@click.option('-a', '--print_available_cities', is_flag=True,
              help='This option print available cities')
@click.option('-fl', '--flexible_dates', is_flag=True,
              help='This option makes dates flexible.\n'
                   'Available flights per week will be printed')
@click.pass_context
def main(search_parameters, print_available_cities, flexible_dates):
    '''This application can search flights\n
    Example input parameters: KHI ISB 02.02.2020 05.02.2020\n
    IATA-code must be three capital letters\n
    Date must be a format DD.MM.YYYY\n'''

    available_cities = AirblueComApi.get_available_cities()
    if print_available_cities:
        print_flights.print_available_cities(available_cities)

    search_parameters = search_parameters.args
    if len(search_parameters) == 0:
        search_parameters = input(
            'Enter the search parameters with a space\n').split()
    while True:
        try:
            flights = search_flights(search_parameters, available_cities,
                                     flexible_dates)
        except (EOFError, KeyboardInterrupt):
            print('Good buy. Thanks for using our app')
            break

        print_flights.print_flights(flights)

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
