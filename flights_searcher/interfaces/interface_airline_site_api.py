from abc import ABC, abstractmethod


class InterfaceAirlineSiteApi(ABC):
    """This class is interface site API classes"""

    @abstractmethod
    def searching_flights(self, iata_from, iata_to, date_on, date_return_on='',
                          flexible_dates_flag=False):
        """This method must implements flights search and returns dictionary"""
        pass

    @abstractmethod
    def get_available_cities(self):
        """This method must returns available cities dictionary"""
        pass
