"""Это модуль, способный произвести поиск авиарейсов и
вывести информацию о них"""

import sys
import warnings
import itertools
from datetime import datetime
import requests
from lxml import html
import click

# Здесь context_settings - словарь с настройками
# allow_extra_args означает,
# Что неизвестные аргументы сохранятся в объекте контекста
@click.command(context_settings=dict(allow_extra_args=True))
# Передача объекта контекста как первого аргумента функции
@click.pass_context
@click.option('-a', '--available_iata',
              help='Показать список доступных IATA-кодов',
              is_flag=True)
def main(input_parametrs, available_iata):
    """Эта команда принимает три обязательных аргумента: IATA-код
         места отправления, IATA-код места прибытия, дату отправления.
        Один необязательный аргумент дату возврата.
        IATA-коды должны быть написаны заглавными буквами,
        даты в формате DD.MM.YYYY. Также доступен флаг -a"""

    if available_iata:
        try:
            data = get_data()
        except requests.exceptions.HTTPError:
            print('Был получен неожиданный код ответа от сервера')
        except requests.exceptions.Timeout:
            print('TimeoutError. Рекомендуется проверить соединение')

        except requests.exceptions.ConnectionError:
            print('ConnectionError. Рекомендуется проверить соединение')

        except requests.exceptions.RequestException as error:
            print('В ходе работы программы возникла ошибка')
            print(error)
        else:
            cities = get_avalible_cities(data)
            print('Список доступных IATA-кодов', *cities)


    if len(input_parametrs.args) != 0:
        search_flights(input_parametrs)


def search_flights(input_parametrs):
    """Эта функция является основной функцией, осуществляющей вызов других
    функция для нахождения рейсов"""

    # Проверим валидность входных параметров
    # В случае ошибки вернём код -1
    try:
        validation_input(input_parametrs.args)
    except ValueError:
        return -1

    # Так как все параметры валидны, составим параметры запроса
    request_parametrs = parse_input_parametrs(*input_parametrs.args)

    # Получим данные с сайта с учётом полученных выше параметров
    try:
        data_flights = get_data(request_parametrs)
    except requests.exceptions.HTTPError:
        print('Был получен неожиданный код ответа от сервера')
        return -1

    except requests.exceptions.Timeout:
        print('TimeoutError. Рекомендуется проверить соединение')
        return -1

    except requests.exceptions.ConnectionError:
        print('ConnectionError. Рекомендуется проверить соединение')
        return -1

    except requests.exceptions.RequestException as error:
        print('В ходе работы программы возникла ошибка')
        print(error)
        return -1

    # Проверим входят ли введённые IATA-коды в список доступных
    try:
        validation_iata_code(data_flights, input_parametrs.args[0],
                             input_parametrs.args[1])
    except ValueError:
        return -1

    # Получим информацию о полётах
    fligts = parse_data_search(data_flights)

    # Если у нас есть четвёртый параметр (дата возврата)
    # То нам нужно составить комбинации рейсов туда-обратно
    # Если нет, то мы просто выведем то, что получили в flights
    if len(input_parametrs.args) == 4:
        comb = combination_fligths(fligts)
        print_result(comb, True)
    else:
        print_result(fligts)

    return 0


def validation_input(parametrs):
    """Эта функция производит проверку входных данных
    на соответствие формату ввода"""

    if len(parametrs) >= 3:
        iata_from = parametrs[0]
        iata_to = parametrs[1]
        date_on = parametrs[2]
    if len(parametrs) == 3:
        date_return_on = ''
    elif len(parametrs) == 4:
        date_return_on = parametrs[2]
    else:
        print('Вы ввели неверное количество параметров')
        raise ValueError('Неверное количество параметров')

    validation_list_date_on = [elem.isdigit()
                               for elem in date_on.split('.')]
    validation_list_date_return_on = [elem.isdigit()
                                      for elem in date_return_on.split('.')]

    if not all(validation_list_date_on) or len(validation_list_date_on) != 3:
        print('Вы ввели некорректное значение даты отправления, '
              'попробуйте снова')
        raise ValueError('Некорректное значение даты отправления')

    elif (date_return_on and (not all(validation_list_date_return_on) or
                              len(validation_list_date_return_on) != 3)):
        print('Вы ввели некорректное значение даты возвращения, '
              'попробуйте снова')
        raise ValueError('Некорректное значение даты возвращения')

    elif not iata_from.isalpha():
        print('Вы ввели некорректный IATA-код места отправления, '
              'попробуйте снова')
        raise ValueError('Некорректный IATA-код места отправления')

    elif not iata_to.isalpha():
        print('Вы ввели некорректный IATA-код места прилёта, '
              'попробуйте снова')
        raise ValueError('Некорректный IATA-код места прилёта')


def validation_iata_code(data, iata_from, iata_to):
    """Эта функция проверяет существование введённых IATA-кодов"""

    avalible_cities = get_avalible_cities(data)
    if iata_from not in avalible_cities or iata_to not in avalible_cities:
        print('Похоже, мы не летаем по такому маршруту. '
              'Список городов, доступных для полёта', *avalible_cities)
        raise ValueError('Несуществующий IATA-код')


def get_avalible_cities(data):
    """Эта функция получает список доступных IATA-кодов"""

    result = data.xpath('.//table[@class="search "]//tr[@class="oneway"]'
                        '//select[@name="AC"]/option/@value')
    return result


def parse_input_parametrs(iata_from, iata_to, date_on, date_return_on=''):
    "Эта функция формирует словарь параметров get-запроса"
    if date_return_on:
        round_trip = 'RT'
    else:
        round_trip = 'OW'

    date_on = date_on.split('.')

    result = {'TT': round_trip, 'DC': iata_from.upper(), 'AC': iata_to.upper(),
              'PA': 1, 'AM': date_on[2] + '-' + date_on[1], 'AD': date_on[0]}

    if date_return_on:
        date_return_on = date_return_on.split('.')
        result['RM'] = date_return_on[2] + '-' + date_return_on[1]
        result['RD'] = date_return_on[0]

    return result


def get_data(parametrs={}):
    """Эта функция осуществляет get-запрос с заданными параметрами"""

    url = 'https://www.airblue.com/bookings/flight_selection.aspx'
    # verify=False - игнорирование ошибок сертификата
    req = requests.get(url, params=parametrs, verify=False)
    # Бросим исключение в случае неожиданного ответа от сервера
    req.raise_for_status()
    return html.fromstring(req.text)


def parse_data_search(data_search):
    """Эта функция составляет список,
    в котором содержится информация о рейсах"""

    trips = data_search.xpath('//div[@class="trip_segment_block fixed-dates"]')
    # В results будут добавлены списки рейсов в каждую из сторон
    results = []
    # Если ни одного trip нет, то мы просто вернём пустой список
    for trip in trips:
        # В flights_in_trip будет добавлена информация о каждом из рейсов
        flights_in_trip = []
        cities = trip.xpath('.//label[@class="city"]/text()')
        flights = trip.xpath('.//table//tbody')

        # При выборе текущей даты, на которую рейсов уже нет,
        # В html с результатами поиска отображается trip, в котором
        # Есть тэг, говорящий об отстутствии результатов
        # Проверим, есть ли этот тег в отданном нам html
        if trip.xpath('.//tr[@class="no_flights_found"]'):
            continue

        for flight in flights:
            # flight_info будет содержать информацию о рейсе
            flight_info = {}
            flight_info['From'] = cities[0].strip()
            flight_info['To'] = cities[2].strip()
            flight_info['Date'] = flight.xpath('../caption/text()')[0].strip()
            flight_info['Flight(s)'] = flight.xpath(
                './/td[@class="flight"]/text()')[0].strip()
            flight_info['Depart'] = flight.xpath(
                './/td[@class="time leaving"]/text()')[0]
            route = flight.xpath('.//td[@class="route"]/span/text()')
            flight_info['Route'] = route[0] + ', ' + route[1]
            flight_info['Arrive'] = flight.xpath(
                './/td[@class="time landing"]/text()')[0]
            flight_info['Class'] = flight.xpath(
                '..//th[@class="family family-ES family-group-Y "]/span/text()'
                )[0].strip()
            price = flight.xpath(
                './/td[@class="family family-ES family-group-Y "]//span')[0]
            flight_info['Price'] = float(price.xpath(
                './text()')[0].strip().replace(',', ''))
            flight_info['Currency'] = price.xpath('./b/text()')[0]
            flights_in_trip.append(flight_info)
        results.append(flights_in_trip)
    return results


def sorted_flights(flights_info):
    """Эта функция сортирует рейсы в каждую сторону по возрастанию цены"""

    for i in range(len(flights_info)):
        flights_info[i].sort(key=lambda flight: flight['Price'])
    return flights_info


def combination_fligths(flights_info):
    """Эта функция составляет комбинации рейсов туда-обратно"""

    flights_info = sorted_flights(flights_info)
    if len(flights_info) == 2:
        result = list(itertools.product(flights_info[0], flights_info[1]))
        return result
    else:
        return []


def sum_price(trip):
    """Эта функция подсчитывает суммарную стоимость перелёта туда-обратно"""

    sum_price_dict = {}
    for flight in trip:
        sum_price_dict[flight['Currency']] = (
            sum_price_dict.setdefault(flight['Currency'], 0) + flight['Price'])
    sum_price_string = ''
    for key, value in sum_price_dict.items():
        sum_price_string += str(value) + ' ' + key + '\n'
    return sum_price_string


def time_in_fly(depart, arrive):
    """Эта функция вычисляет время в полёте для каждого рейса"""

    format_date = '%I:%M %p'
    depart = datetime.strptime(depart, format_date)
    arrive = datetime.strptime(arrive, format_date)
    result = str(arrive - depart).split(':')
    result = f'{result[0]}h {result[1]}m'
    return result


def print_result(flights, print_sum_price=False):
    """Эта функция выводит информацию о найденных рейсах"""

    if not flights:
        print('На выбранные Вами даты рейсов нет')

    else:
        print('Показываю найденные рейсы', end='\n\n')
        for trip in flights:
            for flight in trip:
                print(f'Дата {flight["Date"]}; '
                      f'Откуда {flight["From"]}; '
                      f'Куда {flight["To"]};\n'
                      f'Рейс {flight["Flight(s)"]}; '
                      f'Время вылета {flight["Depart"]}; '
                      f'Время прилёта {flight["Arrive"]};\n'
                      f'Время в полёте '
                      f'{time_in_fly(flight["Depart"], flight["Arrive"])} '
                      f'Пересадки и самолёт {flight["Route"]}; '
                      f'Класс {flight["Class"]}\n'
                      f'Цена {flight["Price"]} {flight["Currency"]}')

            if print_sum_price:
                print(f'Суммарная стоимость "туда-обратно" составляет:\n'
                      f'{sum_price(trip)}')


if __name__ == "__main__":
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    main()
