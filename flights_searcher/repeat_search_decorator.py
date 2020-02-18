import sys


def repeat_search_decorator(func):
    """This decorator implements repeat search"""

    def repeat_search(search_parameters, *args, **kwargs):

        while True:
            func(search_parameters, *args, **kwargs)
            try:
                if input('Search again?(y/n)\n') == 'y':
                    search_parameters = input(
                        'Enter the search parameters with a space\n'
                        'Example input parameters: KHI ISB 02.02.2020 '
                        '05.02.2020\n'
                        'IATA-code must be three capital letters\n'
                        'Date must be a format DD.MM.YYYY\n').split()

                else:
                    print('Good buy. Thanks for using our app')
                    break

            except (EOFError, KeyboardInterrupt):
                print('Good buy. Thanks for using our app')
                sys.exit(0)

    return repeat_search
