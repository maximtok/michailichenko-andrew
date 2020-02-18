from datetime import datetime
from interfaces.interface_validation_classes import InterfaceValidator


class FormatDateValidator(InterfaceValidator):
    """This class implements format date validator"""

    def validating(self, parameter, parameter_name):
        """This method validates format date"""

        try:
            parameter = datetime.strptime(parameter, '%d.%m.%Y').date()

            return super().validating(parameter, parameter_name)

        except ValueError:
            print(f'Error in {parameter_name}: '
                  f'Date must be a format DD.MM.YYYY')

            return False
