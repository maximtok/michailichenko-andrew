from abc import ABC, abstractmethod


class InterfaceFlightsSearcher(ABC):
    """This class is interface flight searchers classes"""

    def __init__(self, context):
        self._context = context

    @abstractmethod
    def searching(self):
        """
        This method must validates input parameters, searches flights and
        handles search result
        """
        pass
