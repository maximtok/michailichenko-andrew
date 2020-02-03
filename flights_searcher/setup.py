from setuptools import setup
setup(
    name='flights_searcher',
    packages=['flights_searcher', 'flights_searcher.lib.airblue_com_api',
              'flights_searcher.lib.search_flights',
              'flights_searcher.lib.validator_input_parameters'],
    entry_points={
        'console_scripts': [
            'flights_searcher = flights_searcher.__main__:main'
        ]
    })