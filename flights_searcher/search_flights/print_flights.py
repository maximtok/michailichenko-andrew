def print_flights(flights):
    if len(flights) == 0:
        print('No flights found for your request')
    else:
        print('Found flights:')
        for round_trip in flights:
            print(*round_trip, sep='\n')


def print_available_cities(available_cities_dict):
    print('Available cities:')
    for iata_code, city_name in available_cities_dict.items():
        print(f'{city_name} ({iata_code})')
