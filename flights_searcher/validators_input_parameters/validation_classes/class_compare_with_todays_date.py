"""This module contains class CompareWithTodaysDate"""

from datetime import date, datetime
from interfaces.interface_validation_classes import InterfaceValidationClasses


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
