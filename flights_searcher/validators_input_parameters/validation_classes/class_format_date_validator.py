"""This module contains class FormatDateValidator"""

from datetime import datetime
from interfaces.interface_validation_classes import InterfaceValidationClasses


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
