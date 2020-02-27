"""This module contains validation classes for chain of responsibility"""

from datetime import date, datetime
from abc import ABC, abstractmethod


class InterfaceValidationClasses(ABC):
    """This class is interface validation classes"""

    _next_validator = None

    def set_next(self, validator):
        """This method sets next validator"""

        self._next_validator = validator

        return validator

    @abstractmethod
    def validating(self, parameter, parameter_name):
        """This method validates parameter and returns result"""

        if self._next_validator:

            return self._next_validator.validating(parameter, parameter_name)

        return True


class CountParametersValidator(InterfaceValidationClasses):
    """This class implements count parameters validator"""

    def validating(self, parameter, parameter_name):
        """This method validates count parameters"""

        if len(parameter) not in (3, 4):
            print(f'Error: You must pass 3 or 4 arguments, '
                  f'not {len(parameter)}')

            return False

        return super().validating(parameter, parameter_name)


class IataCodeCorrectnessValidator(InterfaceValidationClasses):
    """This class implements iata-code correctness validator"""

    def validating(self, parameter, parameter_name):
        """This method validates iata-code correctness"""

        if not (len(parameter) == 3 and parameter.isalpha()
                and parameter.isupper()):
            print(f'Error in {parameter_name}: '
                  f'Invalid IATA-code. IATA-code must '
                  'be three capital letters')
            return False

        return super().validating(parameter, parameter_name)


class IataCodeAvailabilityValidator(InterfaceValidationClasses):
    """This class implements iata-code availability validator"""

    def __init__(self, available_cities):
        super().__init__()
        self.available_cities = available_cities

    def validating(self, parameter, parameter_name):
        """This method validates iata-code availability"""

        if parameter not in self.available_cities:
            print(f'Error in {parameter_name}: '
                  f'This airline does not operate '
                  f'flights from / to {parameter}')

            return False

        return super().validating(parameter, parameter_name)


class InequalityIataCodesValidator(InterfaceValidationClasses):
    """This class implements inequality iata-codes validator"""

    def __init__(self, iata_code_to):
        self.iata_code_to = iata_code_to

    def validating(self, parameter, parameter_name):
        """This method validates inequality iata-codes"""

        if parameter == self.iata_code_to:
            print(f'Error in {parameter_name}: '
                  f'Iata-code to must be != Iata-code from')

            return False

        return super().validating(parameter, parameter_name)


class FormatDateValidator(InterfaceValidationClasses):
    """This class implements format date validator"""

    def validating(self, parameter, parameter_name):
        """This method validates format date"""

        try:
            datetime.strptime(parameter, '%d.%m.%Y').date()

            return super().validating(parameter, parameter_name)

        except ValueError:
            print(f'Error in {parameter_name}: '
                  f'Date must be a format DD.MM.YYYY')

            return False


class CompareWithTodaysDate(InterfaceValidationClasses):
    """This class implements compare date with today's date"""

    def validating(self, parameter, parameter_name):
        """This method compares input_date with today's date"""

        input_parameter = datetime.strptime(parameter, '%d.%m.%Y').date()

        if input_parameter <= date.today():
            print(f'Error in {parameter_name}: '
                  f'Date must be later than today`s date')
            return False

        return super().validating(parameter, parameter_name)


class DateDeltaValidator(InterfaceValidationClasses):
    """This class implements date delta validator"""

    def __init__(self, first_date):
        self.first_date = first_date

    def validating(self, parameter, parameter_name):
        """This method validates date delta"""

        try:
            first_date = datetime.strptime(self.first_date, '%d.%m.%Y').date()

        except ValueError:
            print(f'Error in {parameter_name}: '
                  f'Cannot compare date on and date return on, '
                  f'because date on does not match format DD.MM.YYYY')

            return False

        input_parameter = datetime.strptime(parameter, '%d.%m.%Y').date()

        if input_parameter < first_date:
            print(f'Error in {parameter_name}: '
                  f'Return date must be later '
                  'than departure date')

            return False

        return super().validating(parameter, parameter_name)
