from datetime import datetime, timedelta, date


def validation_count_arguments(arguments):
    if len(arguments) == 3 or len(arguments) == 4:
        result = True
    else:
        raise TypeError(f'Error: You must pass 3 or 4 arguments, '
                        f'not {len(arguments)}')

    return result


def first_validation_iata_code(parametr):
    if len(parametr) == 3 and parametr.isalpha() and parametr.isupper():
        result = True
    else:
        raise ValueError('Error: Invalid IATA-code. IATA-code must '
                         'be three capital letters')

    return result


def second_validation_iata_code(parametr, avaliable_cities):
    if parametr in avaliable_cities:
        result = True
    else:
        string_avaliable_cities = ''
        for key, value in avaliable_cities.items():
            string_avaliable_cities += f'{value} ({key})\n'
        raise ValueError(f'Error: Airline Airblue does not operate '
                         f'flights from / to {parametr}\n'
                         f'Avaliable cities:\n{string_avaliable_cities}')

    return result


def validation_date(parametr):
    format_date = '%d.%m.%Y'
    try:
        result = datetime.strptime(parametr, format_date).date()
    except ValueError:
        raise ValueError('Error: Date must be a format DD.MM.YYYY')

    return result


def comparison_with_todays_date(input_date):
    if input_date >= date.today():
        result = True
    else:
        raise ValueError('Error: Date must be later than today`s date')

    return result


def validation_date_delta(first_date, second_date):
    date_delta = second_date - first_date
    if date_delta >= timedelta():
        result = True
    else:
        raise ValueError(
            'Error: Departure date must be later than return date')

    return result
