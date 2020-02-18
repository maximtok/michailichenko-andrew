from airline_api.class_airblue_com_api import AirblueComApi
from validators_input_parameters.class_validator_iata_codes_and_dates \
    import ValidatorIataCodesAndDates
from handlers.class_handler import Handler


class GlobalContext:
    """
    This class implements global context object

    Global context used to select handler object, airline object and
    validator object
    """

    def __init__(self, parameters, **kwargs):
        self.__dict__.update(kwargs)
        self.parameters = parameters
        self.handler = Handler()
        self.airline_api = AirblueComApi()
        self.validator = ValidatorIataCodesAndDates()
