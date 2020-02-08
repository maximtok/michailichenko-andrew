import warnings
from datetime import datetime, timedelta
from copy import deepcopy
from lxml import html
import requests


class AirblueComApi:

    @staticmethod
    def search_flights(iata_from, iata_to, date_on, date_return_on='',
                       flexible_dates_flag=False):

        parameters = AirblueComApi.__create_parameters_dict(
            iata_from, iata_to,
            date_on, date_return_on, flexible_dates_flag)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            search_page = AirblueComApi.__get_search_page(parameters)

        result = AirblueComApi.__parse_search_page(search_page)

        return result

    @staticmethod
    def get_available_cities():
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            shedule_page = AirblueComApi.__get_shedule_page()

        cities = AirblueComApi.__parse_shedule_page(shedule_page)

        return cities

    @staticmethod
    def __get_search_page(parameters):
        url = 'https://www.airblue.com/bookings/flight_selection.aspx'
        request = requests.get(url, params=parameters)
        request.raise_for_status()

        return html.fromstring(request.text)

    @staticmethod
    def __get_shedule_page():
        url = 'https://www.airblue.com/sched/schedule_popup.asp'
        request = requests.get(url)
        request.raise_for_status()

        return html.fromstring(request.text)

    @staticmethod
    def __create_parameters_dict(iata_from, iata_to,
                                    date_on, date_return_on, flexible_dates):

        date_on = datetime.strftime(date_on, '%d.%m.%Y').split('.')

        result = {'DC': iata_from,
                  'AC': iata_to,
                  'PA': 1, 'AM': date_on[2] + '-' + date_on[1],
                  'AD': date_on[0]}

        if date_return_on:
            result['TT'] = 'RT'
            date_return_on = datetime.strftime(date_return_on,
                                               '%d.%m.%Y').split('.')
            result['RM'] = date_return_on[2] + '-' + date_return_on[1]
            result['RD'] = date_return_on[0]

        else:
            result['TT'] = 'OW'

        if flexible_dates:
            result['FL'] = 'on'

        return result

    @staticmethod
    def __parse_search_page(search_page):
        trips = search_page.xpath(
            './/div[contains(@class, "trip_segment_block") and '
            'contains(@id, "trip")]')

        results = {}

        for number_trip, trip in enumerate(trips, start=1):

            flights = trip.xpath('.//table/tbody')
            flights_in_trip = AirblueComApi.__create_flight_dicts(
                trip, flights)

            results[f'trip_{number_trip}'] = flights_in_trip

        return results

    @staticmethod
    def __create_flight_dicts(trip, flights):

        for flight in flights:
            if flight.xpath('.//tr[@class="no_flights_found"]'):
                continue

            base_flight_dict = AirblueComApi.__create_base_flight_dict(
                trip, flight)
            flight_dicts = AirblueComApi.__append_class_and_price_in_flight_dict(
                flight, base_flight_dict)

            for flight_option in flight_dicts:
                yield flight_option

    @staticmethod
    def __create_base_flight_dict(trip, flight):
        route = flight.xpath('.//td[@class="route"]/span/text()')
        date_flight = flight.xpath('../caption/text()')[0].strip()
        time_depart = flight.xpath(
            './/td[@class="time leaving"]/text()')[0].strip()
        time_arrive_node = flight.xpath(
            './/td[@class="time landing"]')[0]
        time_arrive = time_arrive_node.xpath('./text()')[0].strip()
        delta_date = time_arrive_node.xpath('./sup/text()')

        format_datetime = '%A, %B %d, %Y %I:%M %p'
        depart = datetime.strptime(date_flight + ' ' + time_depart,
                                   format_datetime)
        arrive = datetime.strptime(date_flight + ' ' + time_arrive,
                                   format_datetime)
        if delta_date:
            arrive += timedelta(days=int(delta_date[0].strip()[1:]))

        flight_dict = {
            'from': trip.xpath('.//*[contains(text(), "From")]/'
                               '../text()')[0].strip(),
            'to': trip.xpath('.//*[contains(text(), "To")]/'
                             '../text()')[0].strip(),
            'flight': flight.xpath(
                './/td[@class="flight"]/text()')[0].strip(),
            'depart': depart,
            'route': route[0] + ', ' + route[1],
            'arrive': arrive}

        return flight_dict

    @staticmethod
    def __append_class_and_price_in_flight_dict(flight, base_flight_dict):

        for flight_option in flight.xpath('..//th[contains('
                                          'text(), "Flight(s)")]'
                                          '/following-sibling::th[contains('
                                          '@class, "family")]'):
            flight_option_dict = deepcopy(base_flight_dict)
            class_node = flight_option.xpath('./@class')[0]

            if flight.xpath(f'.//td[@class="{class_node}"]/'
                            f'label[contains(text(),"SOLD OUT")]'):
                continue

            price = flight.xpath(
                f'.//td[@class="{class_node}"]//span')[0]
            flight_option_dict.update({
                'class': flight_option.xpath('./span/text()')[0],
                'price': float(price.xpath(
                    './text()')[0].strip().replace(',', '')),
                'currency': price.xpath('./b/text()')[0]})

            yield flight_option_dict

    @staticmethod
    def __parse_shedule_page(shedule_page):
        options_city_selector = shedule_page.xpath('.//select[@name="origin"]'
                                                   '/option')
        if not options_city_selector:
            raise IndexError

        cities_dict = {option.xpath('./@value')[0]: option.xpath('./@title')[0]
                       for option in options_city_selector}

        return cities_dict

if __name__ == '__main__':
    iata_from = 'JED'
    iata_to = 'LHE'
    date_on = datetime.strptime('10.02.2020', '%d.%m.%Y')
    result = AirblueComApi.search_flights(iata_from, iata_to, date_on)
    print(result)
