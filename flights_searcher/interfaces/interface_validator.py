"""This module contains class InterfaceValidator"""

from abc import ABC, abstractmethod


class InterfaceValidator(ABC):
    """This class is interface validator"""

    def __init__(self, parameters, parameter_names, validators):
        self._parameter_names = parameter_names
        self._validators = validators
        self._parameters = parameters

    @abstractmethod
    def validating_count_parameters(self):
        """This method must implements validating count parameters"""
        pass

    @abstractmethod
    def validating_parameters(self, parameters, available_cities):
        """This method must implements validating parameters"""
        pass
