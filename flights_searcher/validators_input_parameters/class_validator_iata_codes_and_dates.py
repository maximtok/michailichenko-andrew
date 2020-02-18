from validators_input_parameters.validation_classes.\
    class_count_parameters_validator import CountParametersValidator
from validators_input_parameters.validation_classes.\
    class_iata_code_correctness_validator import IataCodeCorrectnessValidator
from validators_input_parameters.validation_classes.\
    class_iata_code_availability_validator import IataCodeAvailabilityValidator
from validators_input_parameters.validation_classes.\
    class_inequality_iata_codes_validator import InequalityIataCodesValidator
from validators_input_parameters.validation_classes.\
    class_format_date_validator import FormatDateValidator
from validators_input_parameters.validation_classes.\
    class_compare_with_todays_date import CompareWithTodaysDate
from validators_input_parameters.validation_classes.\
    class_date_delta_validator import DateDeltaValidator
from interfaces.interface_validator import InterfaceValidator


class ValidatorIataCodesAndDates(InterfaceValidator):
    """
    This class implements validate iata-codes and dates

    As well as, this class gets correct parameters and returns them
    """

    def get_correct_parameters(self, parameters, available_cities):
        """
        This method validates parameters,
        gets correct parameters and returns them
        """

        self._available_cities_string = self.create_available_cities_string(
            available_cities)
        self._available_cities = available_cities

        while True:

            parameters = self._get_correct_count_parameters(parameters)

            validate_results = [False, False, False]

            if len(parameters) == 4:
                validate_results.append(False)

            parameters = self._get_correct_iata_codes_and_dates(
                parameters, validate_results)

            if not self._confirm_search_parameters(parameters):
                parameters = self._repeat_entering_all_parameters()

            else:
                return parameters

    def _get_correct_count_parameters(self, parameters):
        """
        This method validates count parameters and
        gets correct count of parameters
        """

        while True:

            if CountParametersValidator().validating(parameters,
                                                     'Count parameters'):
                return parameters
            else:
                parameters = self._repeat_entering_all_parameters()

    def _get_correct_iata_codes_and_dates(self, parameters, validate_results):
        """
        This method validates iata-codes and dates,
        gets correct iata-codes and dates and returns them
        """

        while True:

            validate_results = self._validating_parameters(parameters,
                                                           validate_results)

            if all(validate_results):
                return parameters

            parameters = self._alter_parameters_list(parameters,
                                                     validate_results)

    def _validating_parameters(self, parameters, validate_results):
        """This method validates iata-codes and dates"""

        if not validate_results[0]:
            validate_results[0] = self._validating_iata_code_from(
                parameters[0], self._parameter_names[0])

        if not validate_results[1]:
            validate_results[1] = self._validating_iata_code_to(
                parameters[1], self._parameter_names[1], parameters[0])

        if not validate_results[2]:
            validate_results[2] = self._validating_date_on(
                parameters[2], self._parameter_names[2])

        if len(parameters) == 4 and not validate_results[3]:
            validate_results[3] = self._validating_date_return_on(
                parameters[3], self._parameter_names[3], parameters[2])

        return validate_results

    @staticmethod
    def _repeat_entering_all_parameters():
        """This method gets parameters form user and returns them"""

        return input('Enter the search parameters with a space\n'
                     'Example input parameters: '
                     'KHI ISB 02.02.2020 05.02.2020\n'
                     'IATA-code must be three capital letters\n'
                     'Date must be a format DD.MM.YYYY\n').split()

    def _repeat_entering_incorrect_parameters(self, validate_results):
        """This method gets incorrect parameters form user"""

        hint_string = self._create_hint_string(validate_results)
        return input(hint_string + '\n').split()

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

    def _create_hint_string(self, validate_results):
        """This method creates hint string for incorrect parameters"""

        incorrect_parameters_list = [self._parameter_names[index] for
                                     index in range(len(validate_results))
                                     if not validate_results[index]]

        if all(validate_results[:2]):
            result = 'Please, enter '
        else:
            result = self._available_cities_string + '\nPlease, enter '

        result += ', '.join(incorrect_parameters_list)

        return result

    def _confirm_search_parameters(self, parameters):
        """This method confirms search parameters"""

        print('Are your parameters correct?(y/n)')
        for index, parameter in enumerate(parameters):
            print(f'{self._parameter_names[index]}: {parameter}')

        return input() == 'y'

    def _validating_iata_code_from(self, parameter, parameter_name):
        """This method validates iata-code from"""

        validator_iata_code_correctness = IataCodeCorrectnessValidator()
        validator_iata_code_availability = IataCodeAvailabilityValidator(
            self._available_cities)

        validator_iata_code_correctness.set_next(
            validator_iata_code_availability)

        return validator_iata_code_correctness.validating(
            parameter, parameter_name)

    def _validating_iata_code_to(self, parameter, parameter_name,
                                 iata_code_from):
        """This method validates iata-code to"""

        validator_iata_code_correctness = IataCodeCorrectnessValidator()
        validator_iata_code_availability = IataCodeAvailabilityValidator(
            self._available_cities)
        validator_inequality_iata_codes = InequalityIataCodesValidator(
            iata_code_from)

        validator_iata_code_correctness.set_next(
            validator_iata_code_availability)
        validator_iata_code_availability.set_next(
            validator_inequality_iata_codes)

        return validator_iata_code_correctness.validating(
            parameter, parameter_name)

    @staticmethod
    def _validating_date_on(parameter, parameter_name):
        """This method validates date on"""

        validator_format_date = FormatDateValidator()
        compare_with_todays_date = CompareWithTodaysDate()

        validator_format_date.set_next(compare_with_todays_date)

        return validator_format_date.validating(parameter, parameter_name)

    @staticmethod
    def _validating_date_return_on(parameter, parameter_name, date_on):
        """This method validates date return on"""

        validator_format_date = FormatDateValidator()
        compare_with_todays_date = CompareWithTodaysDate()
        validator_date_delta = DateDeltaValidator(date_on)

        validator_format_date.set_next(compare_with_todays_date)
        compare_with_todays_date.set_next(validator_date_delta)

        return validator_format_date.validating(parameter, parameter_name)
