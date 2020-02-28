# Flight searcher
Command line application for search flights

# How to use it?
This application runs by running the file main.py

For example:

python main.py JED LHE 02.02.2020 05.02.2020

### Parameters
first parameter - IATA-code from

second parameter - IATA-code to

third parameter - Date on

fourth parameter - Date return on (optional)

### Flags
-a, --print_available_cities - this option prints available cities

-fl, --flexible_dates - this option makes dates flexible. Available flights per week will be printed

# Getting Started
This section provides a high-level quick start guide.

You need to use git clone for download flight searcher

### Prerequisites
- [python](https://www.python.org/): we recommend using the python version 3.7.x
- [click](https://click.palletsprojects.com/): we recommend using the click version 7.x
- [lxml](https://lxml.de/): we recommend using the lxml version 4.4.x
- [requests](https://requests.readthedocs.io/): we recommend using the requests version 2.22.x
