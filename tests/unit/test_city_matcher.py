import pytest
from CityAutoCompleter.CityAutoCompleter import CityAutoCompleter

def test_city_search_with_no_optional_params():
    city_search = CityAutoCompleter()
    results = city_search.suggest("chi")
    assert results[0]['name'] == "Chino"

def test_city_search_with_lat_long():
    city_search = CityAutoCompleter()
    results = city_search.suggest("chi", user_lat=41.84, user_lon=-87.65)
    assert results[0]['name'] == "Chicago"

