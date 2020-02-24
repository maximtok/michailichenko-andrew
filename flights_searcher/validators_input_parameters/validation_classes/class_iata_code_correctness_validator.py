"""This module contains class IataCodeCorrectnessValidator"""

from interfaces.interface_validation_classes import InterfaceValidationClasses


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
