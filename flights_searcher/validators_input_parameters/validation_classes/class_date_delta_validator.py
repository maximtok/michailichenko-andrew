from datetime import datetime
from interfaces.interface_validation_classes import InterfaceValidator


class DateDeltaValidator(InterfaceValidator):
    """This class implements date delta validator"""

    def __init__(self, first_date):
        self.first_date = first_date

    def validating(self, parameter, parameter_name):
        """This method validates date delta"""

        try:
            first_date = datetime.strptime(self.first_date, '%d.%m.%Y').date()
            print(first_date)
        except ValueError:
            print(f'Error in {parameter_name}: '
                  f'Cannot compare date on and date return on, '
                  f'because date on does not match format DD.MM.YYYY')

            return False

        if parameter < first_date:
            print(f'Error in {parameter_name}: '
                  f'Return date must be later '
                  'than departure date')

            return False

        else:

            return super().validating(parameter, parameter_name)
