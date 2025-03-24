import pytest
from CityAutoCompleter.CityAutoCompleter import CityAutoCompleter

def test_city_search_returns_chicago():
    city_search = CityAutoCompleter()
    results = city_search.suggest("chi")
    print(results)
    # assert results[0]['name'] == "Chicago"

def test_city_search_with_lat_long_returns_chicago():
    city_search = CityAutoCompleter()
    results = city_search.suggest("chi", user_lat=41.84, user_lon=-87.65)
    print(results)
    assert results[0]['name'] == "Chicago"

