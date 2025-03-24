import pandas as pd
from rapidfuzz import process
from geopy.distance import geodesic

class FuzzyCitySearch:
    def __init__(self):
        """
        Initialize the fuzzy search class with a CSV dataset.
        """
        self.df = pd.read_csv('cities_canada-usa.tsv', sep='\t')
        self._clean_columns()
    
    def _clean_columns(self):
        """Standardizes column names to lowercase and removes spaces."""
        self.df.columns = self.df.columns.str.strip().str.lower()

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Returns the geodesic distance (in km) between two lat/lon points."""
        return geodesic((lat1, lon1), (lat2, lon2)).km

    def search(self, query, query_lat=None, query_lon=None, top_n=5):
        """
        Performs fuzzy city name search with optional geographic filtering.

        :param query: Partial/full city name to search.
        :param query_lat: (Optional) Latitude to rank results by proximity.
        :param query_lon: (Optional) Longitude to rank results by proximity.
        :param top_n: Number of top matches to return.
        :return: List of dictionaries with matched city names, scores, and distances.
        """
        if 'name' not in self.df.columns or 'lat' not in self.df.columns or 'long' not in self.df.columns:
            raise ValueError("CSV file must contain 'name', 'latitude', and 'longitude' columns.")
        
        # Perform fuzzy matching on city names
        matches = process.extract(query, self.df['name'], limit=top_n)
        matches = [(match[0], round(match[1] / 100, 2)) for match in matches]

        results = []
        for match in matches:
            city_name, score = match[0], match[1]
            city_data = self.df[self.df['name'] == city_name].iloc[0]
            city_lat, city_lon = city_data['lat'], city_data['long']

            # Compute distance if lat/lon is provided
            distance = None
            if query_lat is not None and query_lon is not None:
                distance = self._calculate_distance(query_lat, query_lon, city_lat, city_lon)

            results.append({
                'name': city_name,
                'score': score,
                'latitude': city_lat,
                'longitude': city_lon,
                'distance_km': distance
            })
        
        # sort results descending
        if query_lat is not None and query_lon is not None:
            results.sort(key=lambda x: (-x['score'], x['distance_km']))
        else:
            results.sort(key=lambda x: -x['score'])

        return results

if __name__ == "__main__":
    city_search = FuzzyCitySearch()
    
    # Example: Search for "New" (e.g., New York, New Orleans) without location data
    results = city_search.search("New")
    print("Search results without lat/lon filtering:")
    for r in results:
        print(r)

    # Example: Search for "New" with location data (NYC lat/lon)
    results_with_geo = city_search.search("New", query_lat=40.7128, query_lon=-74.0060)
    print("\nSearch results with lat/lon filtering:")
    for r in results_with_geo:
        print(r)
