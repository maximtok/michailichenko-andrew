"""This module contains main function"""

import sys
import click
from search_flights import searching_flights


@click.command(context_settings=dict(allow_extra_args=True))
@click.option('-a', '--print_available_cities', is_flag=True,
              help='This option prints available cities')
@click.option('-fl', '--flexible_dates', is_flag=True,
              help='This option makes dates flexible.\n'
                   'Available flights per week will be printed')
@click.pass_context
def main(search_parameters, print_available_cities, flexible_dates):
    """
    This application can search flights\n
    Example input parameters: KHI ISB 02.02.2020 05.02.2020\n
    IATA-code must be three capital letters\n
    Date must be a format DD.MM.YYYY\n
    """

    searching_flights(search_parameters.args,
                      print_available_cities_flag=print_available_cities,
                      flexible_dates_flag=flexible_dates)

    sys.exit(0)


if __name__ == '__main__':
    main()
