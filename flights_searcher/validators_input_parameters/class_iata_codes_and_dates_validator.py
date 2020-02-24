"""This module contains class ValidatorIataCodesAndDates"""

from interfaces.interface_validator import InterfaceValidator


class ValidatorIataCodesAndDates(InterfaceValidator):
    """This class implements validate iata-codes and dates"""

    def validating_count_parameters(self):
        """This method validates count parameters"""

        return self._validators[0].validating(self._parameters,
                                              self._parameter_names[0])

    def validating_parameters(self):
        """
        This method validates parameters and
        returns validation results list
        """

        validation_results = []

        for index, parameter in enumerate(self._parameters, start=1):

            validation_result = self._validators[index].validating(
                parameter, self._parameter_names[index])
            validation_results.append(validation_result)

        return validation_results
