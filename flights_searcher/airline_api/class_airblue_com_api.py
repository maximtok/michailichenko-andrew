from datetime import datetime, timedelta
from copy import deepcopy
from lxml import html
import requests
from interfaces.interface_airline_site_api import InterfaceAirlineSiteApi


class AirblueComApi(InterfaceAirlineSiteApi):
    """This class implements Airblue airline site API"""

    def searching_flights(self, iata_from, iata_to, date_on, date_return_on='',
                          flexible_dates_flag=False):
        """This method implements flights search"""

        parameters = self._create_parameters_dict(
            iata_from, iata_to,
            date_on, date_return_on, flexible_dates_flag)
        url = 'https://www.airblue.com/bookings/flight_selection.aspx'
        search_page = self.get_page(url, parameters)

        return self._parse_search_page(search_page)

    def get_available_cities(self):
        """This method returns available cities dictionary"""

        url = 'https://www.airblue.com/sched/schedule_popup.asp'
        schedule_page = self.get_page(url)

        return self._parse_schedule_page(schedule_page)

    @staticmethod
    def get_page(url, parameters=None):
        """This method gets page by url"""

        if parameters is None:
            parameters = {}

        request = requests.get(url, params=parameters, timeout=5)
        request.raise_for_status()

        return html.fromstring(request.text)

    @staticmethod
    def _create_parameters_dict(iata_from, iata_to,
                                date_on, date_return_on, flexible_dates):
        """This method creates search parameters dictionary for request"""

        date_on = date_on.split('.')

        result = {'DC': iata_from,
                  'AC': iata_to,
                  'PA': 1, 'AM': date_on[2] + '-' + date_on[1],
                  'AD': date_on[0]}

        if date_return_on:
            result['TT'] = 'RT'

            date_return_on = date_return_on.split('.')
            result['RM'] = date_return_on[2] + '-' + date_return_on[1]
            result['RD'] = date_return_on[0]

        else:
            result['TT'] = 'OW'

        if flexible_dates:
            result['FL'] = 'on'

        return result

    def _parse_search_page(self, search_page):
        """This method parses search page and returns trips list"""

        trips = search_page.xpath(
            './/div[contains(@class, "trip_segment_block") and '
            'contains(@id, "trip")]')

        results = {}

        for number_trip, trip in enumerate(trips, start=1):

            flights = trip.xpath('.//table/tbody')
            flights_in_trip = self._create_flight_dicts_generator(
                trip, flights)

            results[f'trip_{number_trip}'] = flights_in_trip

        return results

    def _create_flight_dicts_generator(self, trip, flights):
        """This method creates flight dictionary generator"""

        for flight in flights:
            if flight.xpath('.//tr[@class="no_flights_found"]'):
                continue

            base_flight_dict = self._create_base_flight_dict(
                trip, flight)
            flight_dicts = self._append_class_and_price_to_flight_dict(
                flight, base_flight_dict)

            for flight_option in flight_dicts:
                yield flight_option

    @staticmethod
    def _create_base_flight_dict(trip, flight):
        """This method creates base flight dictionary"""

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
    def _append_class_and_price_to_flight_dict(flight,
                                               base_flight_dict):
        """
        This method appends class and price to flight dictionary and returns
        generator of different tickets
        """

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
    def _parse_schedule_page(schedule_page):
        """
        This method parses schedule page and returns
        available cities dictionary
        """

        options_city_selector = schedule_page.xpath('.//select[@name="origin"]'
                                                    '/option')

        cities_dict = {option.xpath('./@value')[0]: option.xpath('./@title')[0]
                       for option in options_city_selector}

        return cities_dict
