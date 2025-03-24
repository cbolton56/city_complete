import pandas as pd
import math
from rapidfuzz import fuzz

class CityAutoCompleter:
    def __init__(self):
        """
        Load cities from a .tsv file using pandas.
        The file must contain columns: 'name', 'lat', 'long'
        """
        self.df = pd.read_csv('cities_canada-usa.tsv', usecols=['name', 'lat', 'long'], sep='\t')
        self.df.dropna(subset=['name', 'lat', 'long'], inplace=True)

    def _haversine(self, lat1, lon1, lat2, lon2):
        """Calculates haversine distance."""
        R = 6371  # Earth radius in km
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lon2 - lon1)
        a = math.sin(d_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            
    def suggest(self, prefix, user_lat=None, user_lon=None, top_n=5):
        prefix_lower = prefix.lower()

        def compute_scores(row):
            name = row['name']
            lat, lon = row['lat'], row['long']
            name_lower = name.lower()

            # matches to prefix
            if name_lower.startswith(prefix_lower):
                match_len = len(prefix)
                total_len = len(name)
                name_score = (match_len / total_len) * 100
            else:
                # since we are doing auto complete, we want to match to prefix
                name_score = 0 

            # add distance calculation and weight
            if user_lat is not None and user_lon is not None:
                distance = self._haversine(user_lat, user_lon, lat, lon)
                distance_score = max(0, 100 - distance)
            else:
                distance = None
                distance_score = 50  # neutral if no location

            # use a linear combination to get a score, normalize between 0 and 1
            confidence = round((0.7 * name_score + 0.3 * distance_score) / 100, 4)

            return pd.Series({
                'name': name,
                'distance_km': round(distance, 2) if distance is not None else None,
                'confidence': confidence,
                'name_score': name_score
            })

        scores_df = self.df.copy()
        scores_df[['name', 'distance_km', 'confidence', 'name_score']] = scores_df.apply(compute_scores, axis=1)

        filtered_df = scores_df[scores_df['name_score'] > 0]

        return filtered_df.sort_values('confidence', ascending=False).head(top_n)[
            ['name', 'distance_km', 'confidence']
        ].to_dict(orient='records')
