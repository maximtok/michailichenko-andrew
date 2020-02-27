"""This module contains class ParametersGetter"""


class ParametersGetter:
    """This class implements parameters getter"""

    def __init__(self, parameter_names, available_cities):
        self._parameter_names = parameter_names
        self.available_cities_string = self._create_available_cities_string(
            available_cities)

    def get_correct_parameters(self, validator, parameters):
        """
        This method gets correct parameters and returns them
        If all parameters correct, then this method returns None
        """

        if not validator.validating_count_parameters():

            return self._repeat_entering_all_parameters()

        validate_results = validator.validating_parameters()
        if not all(validate_results):

            return self._alter_parameters_list(parameters, validate_results)

        return True

    def confirm_search_parameters(self, parameters):
        """This method confirms search parameters"""

        print('Are your parameters correct?(y/n)')
        for index, parameter in enumerate(parameters):
            print(f'{self._parameter_names[index + 1]}: {parameter}')

        if input() == 'y':
            return True

        return self._repeat_entering_all_parameters()

    @staticmethod
    def _repeat_entering_all_parameters():
        """This method gets parameters form user and returns them"""

        return input('Enter the search parameters with a space\n'
                     'Example input parameters: '
                     'KHI ISB 02.02.2020 05.02.2020\n'
                     'IATA-code must be three capital letters\n'
                     'Date must be a format DD.MM.YYYY\n').split()

    def _alter_parameters_list(self, parameters, validate_results):
        """
        This method replaces incorrect parameters with new ones and
        returns parameters list
        """

        while True:

            new_parameters = self._repeat_entering_incorrect_parameters(
                validate_results)

            try:
                for index, validate_result in enumerate(validate_results):
                    if not validate_result:
                        parameters[index] = new_parameters.pop(0)

                break

            except IndexError:
                print('Error: You did not enter all the required parameters')

        return parameters

    def _repeat_entering_incorrect_parameters(self, validate_results):
        """This method gets incorrect parameters form user"""

        hint_string = self._create_hint_string(validate_results)

        return input(hint_string + '\n').split()

    def _create_hint_string(self, validate_results):
        """This method creates hint string for incorrect parameters"""

        incorrect_parameters_list = [self._parameter_names[index + 1] for
                                     index in range(len(validate_results))
                                     if not validate_results[index]]

        if all(validate_results[:2]):
            result = 'Please, enter '
        else:
            result = self.available_cities_string + '\nPlease, enter '

        result += ', '.join(incorrect_parameters_list)

        return result

    @staticmethod
    def _create_available_cities_string(available_cities_dict):
        """This method creates available cities string"""

        result_string = 'Available cities:\n'
        result_string += '\n'.join([f'{city_name} ({iata_code})'
                                    for iata_code, city_name
                                    in available_cities_dict.items()])
        return result_string
