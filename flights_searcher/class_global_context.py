"""This module contains class GlobalContext"""

from airline_api.class_airblue_com_api import AirblueComApi
from validators_input_parameters.class_iata_codes_and_dates_validator \
    import ValidatorIataCodesAndDates
from handlers.class_handler import Handler
from validators_input_parameters import validation_classes
from parameters_getter.class_parameters_getter import ParametersGetter


class GlobalContext:
    """
    This class implements global context object

    Global context used to select handler object, airline object and
    validator object
    """

    def __init__(self, parameters, **kwargs):
        self.__dict__.update(kwargs)
        self.parameters = parameters
        self._parameter_names = ['Count parameters', 'IATA-code from',
                                 'IATA-code to', 'Date on', 'Date return on']
        self.airline_api = AirblueComApi()
        self.handler = Handler()

        self.available_cities = self.airline_api.get_available_cities()

        self.parameters_getter = ParametersGetter(self._parameter_names,
                                                  self.available_cities)

        self.validator = ValidatorIataCodesAndDates(
            self.parameters, self._parameter_names,
            self._create_parameter_validators_list())

    def set_new_parameters(self, parameters):
        """This method sets new parameters and sets new validator"""

        self.parameters = parameters
        self.validator = ValidatorIataCodesAndDates(
            self.parameters, self._parameter_names,
            self._create_parameter_validators_list())

    def _create_parameter_validators_list(self):
        """This method creates parameters validators list"""

        result = [validation_classes.CountParametersValidator()]

        if len(self.parameters) in (3, 4):
            result.extend([self._create_iata_code_from_validator(),
                           self._create_iata_code_to_validator(),
                           self._create_date_on_validator()])

        if len(self.parameters) == 4:
            result.append(self._create_date_return_on_validator())

        return result

    def _create_iata_code_from_validator(self):
        """This method creates chain iata-code from validation"""

        validator_iata_code_correctness = validation_classes.\
            IataCodeCorrectnessValidator()
        validator_iata_code_availability = validation_classes.\
            IataCodeAvailabilityValidator(self.available_cities)

        validator_iata_code_correctness.set_next(
            validator_iata_code_availability)

        return validator_iata_code_correctness

    def _create_iata_code_to_validator(self):
        """This method creates chain iata-code to validation"""

        validator_iata_code_correctness = validation_classes.\
            IataCodeCorrectnessValidator()
        validator_iata_code_availability = validation_classes.\
            IataCodeAvailabilityValidator(self.available_cities)
        validator_iata_codes_inequality = validation_classes.\
            InequalityIataCodesValidator(self.parameters[0])

        validator_iata_code_correctness.set_next(
            validator_iata_code_availability)
        validator_iata_code_availability.set_next(
            validator_iata_codes_inequality)

        return validator_iata_code_correctness

    @staticmethod
    def _create_date_on_validator():
        """This method creates chain date on validation"""

        validator_format_date = validation_classes.FormatDateValidator()
        compare_with_todays_date = validation_classes.CompareWithTodaysDate()

        validator_format_date.set_next(compare_with_todays_date)

        return validator_format_date

    def _create_date_return_on_validator(self):
        """This method creates chain date return on validation"""

        validator_format_date = validation_classes.FormatDateValidator()
        compare_with_todays_date = validation_classes.CompareWithTodaysDate()
        validator_date_delta = validation_classes.DateDeltaValidator(
            self.parameters[2])

        validator_format_date.set_next(compare_with_todays_date)
        compare_with_todays_date.set_next(validator_date_delta)

        return validator_format_date
