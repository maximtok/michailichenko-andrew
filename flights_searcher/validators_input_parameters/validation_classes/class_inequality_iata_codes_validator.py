"""This module contains class InequalityIataCodesValidator"""

from interfaces.interface_validation_classes import InterfaceValidationClasses


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
