from interfaces.interface_validation_classes import InterfaceValidator


class InequalityIataCodesValidator(InterfaceValidator):
    """This class implements inequality iata-codes validator"""

    def __init__(self, iata_code_from):
        self.iata_code_to = iata_code_from

    def validating(self, parameter, parameter_name):
        """This method validates inequality iata-codes"""

        if parameter == self.iata_code_to:
            print(f'Error in {parameter_name}: '
                  f'Iata-code to must be != Iata-code from')

            return False

        else:

            return super().validating(parameter, parameter_name)
