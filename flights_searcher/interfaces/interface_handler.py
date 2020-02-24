"""This module contains class InterfaceHandler"""

from abc import ABC, abstractmethod


class InterfaceHandler(ABC):
    """This class is interface handler classes"""

    @abstractmethod
    def handle(self, dict_result_search):
        """This method must handles search flights result dictionary"""
        pass
