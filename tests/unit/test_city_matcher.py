import pytest
from FuzzyCitySearch.FuzzyCitySearch import FuzzyCitySearch

def test_city_search_with_no_lat_long():
    city_search = FuzzyCitySearch()
    results = city_search.search("New")
    print(results)

def test_city_search_with_lat_long():
    city_search = FuzzyCitySearch()
    results = city_search.search("New", query_lat=40.12, query_long=-74.02)
    print(results)
