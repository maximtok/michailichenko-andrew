def print_flights(flights):
    if len(flights) == 0:
        print('No flights found for your request')
    else:
        print('Found flights:')
        for round_trip in flights:
            print(*round_trip, sep='\n')
