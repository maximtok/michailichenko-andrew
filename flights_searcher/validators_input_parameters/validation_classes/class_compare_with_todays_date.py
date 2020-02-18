from datetime import date
from interfaces.interface_validation_classes import InterfaceValidator


class CompareWithTodaysDate(InterfaceValidator):
    """This class implements compare date with today's date"""

    def validating(self, parameter, parameter_name):
        """This method compares input_date with today's date"""

        if parameter <= date.today():
            print(f'Error in {parameter_name}: '
                  f'Date must be later than today`s date')
            return False

        else:

            return super().validating(parameter, parameter_name)
