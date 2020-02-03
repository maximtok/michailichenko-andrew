from ..airblue_com_api.class_airblue_com_api import AirblueComApi
from ..validator_input_parameters import validation_functions


def validation_search_parameters(arguments):
    avaliable_cities = AirblueComApi.avaliable_cities()
    while True:
        try:
            arguments = re_input_all_arguments(arguments)

            for i in range(len(arguments)):
                arguments = re_input_one_argument(arguments, i,
                                                  avaliable_cities)

            if len(arguments) == 4:
                arguments = re_input_dates(arguments)

            print('Check for correctness your search parameters', sep='\n')
            parameters_for_checking = [f'{parameter[0]}: {parameter[1]}'
                                       for parameter in zip(['departure',
                                                             'arrival',
                                                             'date on',
                                                             'date return on'],
                                                            arguments)]
            print(*parameters_for_checking, sep='\n')

            if input('Are your parameters is a correct? (y/n)\n') == 'y':
                break
            else:
                arguments = input('Enter the search parameters '
                                  'with a space\n').split()
        except EOFError:
            print('Good buy. Thanks for using our app')
            raise EOFError

    return arguments


def re_input_all_arguments(arguments):
    while True:
        try:
            validation_functions.validation_count_arguments(arguments)
            break
        except TypeError as error:
            print(error)
            arguments = input('Enter the search parameters '
                              'with a space\n').split()

    return arguments


def re_input_one_argument(arguments, index, avaliable_cities=None):
    argument_names = {0: 'departure IATA-code', 1: 'iata to',
                      2: 'date on', 3: 'date return on'}

    if index <= 1:
        while True:
            try:
                validation_functions.first_validation_iata_code(
                    arguments[index])
                validation_functions.second_validation_iata_code(
                    arguments[index], avaliable_cities)
                break
            except ValueError as error:
                print(error)
                arguments[index] = input(f'Enter a new '
                                         f'{argument_names[index]}\n')
    else:
        while True:
            try:
                arguments[index] = validation_functions.validation_date(
                    arguments[index])
                validation_functions.comparison_with_todays_date(
                    arguments[index])
                break
            except ValueError as error:
                print(error)
                arguments[index] = input(f'Enter a new '
                                         f'{argument_names[index]}\n')

    return arguments


def re_input_dates(arguments):
    argument_names = {2: 'date on', 3: 'date return on'}
    while True:
        try:
            validation_functions.validation_date_delta(
                arguments[2], arguments[3])
            return arguments
        except ValueError as error:
            print(error)
            arguments[2] = input(f'Enter a new {argument_names[2]}\n')
            arguments = re_input_one_argument(arguments, 2)
            arguments[3] = input(f'Enter a new {argument_names[3]}\n')
            arguments = re_input_one_argument(arguments, 3)
