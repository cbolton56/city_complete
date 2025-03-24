from rapidfuzz import process
from geopy.distance import geodesic
import pandas as pd

# Function to calculate distance between two lat/lon points
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

# Function for fuzzy search with optional lat/long
def fuzzy_search_with_geo(query, query_lat=None, query_lon=None, df=None, top_n=5):
    # Case 1: Query with only a city name
    if query_lat is None or query_lon is None:
        # Perform fuzzy matching for city name
        matches = process.extract(query, df['name'], limit=top_n)
        
        results = []
        for match in matches:
            city_name = match[0]
            score = match[1]
            city_data = df[df['name'] == city_name].iloc[0]
            results.append({
                'city': city_name,
                'score': score,
                'latitude': city_data['latitude'],
                'longitude': city_data['longitude'],
                'distance_km': None  # No distance calculated
            })
        return results
    
    # query with both a city name and lat/long data
    else:
        # city name fuzzy match algorithm
        matches = process.extract(query, df['name'], limit=top_n)

        results = []
        for match in matches:
            city_name = match[0]
            score = match[1]
            
            # Get latitude and longitude of the matched city
            city_data = df[df['name'] == city_name].iloc[0]
            city_lat = city_data['latitude']
            city_lon = city_data['longitude']

            # distance from the query location
            distance = calculate_distance(query_lat, query_lon, city_lat, city_lon)

            results.append({
                'city': city_name,
                'score': score,
                'latitude': city_lat,
                'longitude': city_lon,
                'distance_km': distance
            })
        
        # sort results by fuzzy score
        results.sort(key=lambda x: (x['score'], -x['distance_km'] if query_lat else 0), reverse=True)
        return results

df = pd.read_csv('cities_canada-usa.tsv', sep='\t')

# Test Case 1: Only a city name (no lat/long provided)
query = "New"
result = fuzzy_search_with_geo(query, df=df)

# Test Case 2: City name with lat/long data
query = "New"
query_lat = 40.7128  # Example: New York's lat
query_lon = -74.0060  # Example: New York's lon
result_with_geo = fuzzy_search_with_geo(query, query_lat=query_lat, query_lon=query_lon, df=df)

# Display results for both cases
print("Results for City Name Search:")
for city in result:
    print(city)

print("\nResults for City Name + Geo Search:")
for city in result_with_geo:
    print(city)
