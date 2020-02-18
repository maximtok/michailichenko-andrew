from interfaces.interface_validation_classes import InterfaceValidator


class CountParametersValidator(InterfaceValidator):
    """This class implements count parameters validator"""

    def validating(self, parameter, parameter_name):
        """This method validates count parameters"""

        if len(parameter) not in (3, 4):
            print(f'Error: You must pass 3 or 4 arguments, '
                  f'not {len(parameter)}')

            return False

        else:

            return super().validating(parameter, parameter_name)
