"""This module contains class InterfaceValidationClasses"""

from abc import ABC, abstractmethod


class InterfaceValidationClasses(ABC):
    """This class is interface validation classes"""

    _next_validator = None

    def set_next(self, validator):
        """This method sets next validator"""

        self._next_validator = validator

        return validator

    @abstractmethod
    def validating(self, parameter, parameter_name):
        """This method validates parameter and returns result"""

        if self._next_validator:

            return self._next_validator.validating(parameter, parameter_name)

        return True
