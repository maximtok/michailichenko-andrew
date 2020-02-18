from interfaces.interface_validation_classes import InterfaceValidator


class IataCodeAvailabilityValidator(InterfaceValidator):
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

        else:

            return super().validating(parameter, parameter_name)
