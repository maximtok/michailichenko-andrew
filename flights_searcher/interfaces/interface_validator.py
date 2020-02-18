from abc import ABC, abstractmethod


class InterfaceValidator(ABC):
    def __init__(self):
        self._parameter_names = ['IATA-code from', 'IATA-code to', 'Date on',
                                 'Date return on']


    @staticmethod
    def create_available_cities_string(available_cities_dict):
        """This method creates available cities string"""

        result_string = 'Available cities:\n'
        result_string += '\n'.join([f'{city_name} ({iata_code})'
                                    for iata_code, city_name
                                    in available_cities_dict.items()])
        return result_string

    @abstractmethod
    def get_correct_parameters(self, parameters, available_cities):
        pass
