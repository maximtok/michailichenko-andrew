"""This module contains class InterfaceParametersGetter"""

from abc import ABC, abstractmethod


class InterfaceParametersGetter(ABC):
    """This class is interface parameters getter"""

    def __init__(self, parameter_names, available_cities):
        self._parameter_names = parameter_names
        self.available_cities_string = self._create_available_cities_string(
            available_cities)

    @abstractmethod
    def get_correct_parameters(self, validator, parameters):
        """This method must implements get correct parameters"""
        pass

    @abstractmethod
    def confirm_search_parameters(self, parameters):
        """This method must implements confirm search parameters"""
        pass

    @staticmethod
    def _create_available_cities_string(available_cities_dict):
        """This method creates available cities string"""

        result_string = 'Available cities:\n'
        result_string += '\n'.join([f'{city_name} ({iata_code})'
                                    for iata_code, city_name
                                    in available_cities_dict.items()])
        return result_string
