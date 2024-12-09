import requests
import math
from datetime import datetime, timedelta
import time
import pandas as pd

class fetch_data:
    def __init__(self):
        self.api_key = 'PzSCwucThlnuShzYSBWvZHOAZqvoWGlV'
        self.base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2'
        self.headers = {'token': self.api_key}

    def fetch_station(self, latitude, longitude):

        def calculate_lat_lon_box(center_lat, center_lon, miles):
            # Convert square miles to the side length of the square
            side_length = miles  # Side length in miles

            # Latitude change (1 degree latitude = 69 miles)
            delta_lat = side_length / 69.0

            # Longitude change
            miles_per_degree_lon = 69.0 * math.cos(math.radians(center_lat))
            delta_lon = side_length / miles_per_degree_lon

            def check(val):
                if val > 180:
                    return (-180 + val - 180)
                if val < -180:
                    return (180 - val + 180)
                else:
                    return val

            lower_lat = check(center_lat-delta_lat)
            upper_lat = check(center_lat+delta_lat)
            lower_lon = check(center_lon-delta_lon)
            upper_lon = check(center_lon+delta_lon)

            return (lower_lat, lower_lon), (upper_lat, upper_lon)

        def haversine_spherical_distance(coord1, coord2):
            # Earth's radius in kilometers
            R = 6371.0

            # Convert latitude and longitude from degrees to radians
            lat1, lon1 = map(math.radians, coord1)
            lat2, lon2 = map(math.radians, coord2)

            # Differences in coordinates
            dlat = lat2 - lat1
            dlon = lon2 - lon1

            # Haversine formula
            a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

            # Distance in kilometers --> miles
            distance = R * c * 0.621371

            return distance


        # The endpoint for searching stations by location (latitude and longitude)
        endpoint = '/stations'
        url = self.base_url + endpoint

        miles = 50
        change = 10
        continue_loop = 1
        while continue_loop == 1:
            status = 0
            extent = calculate_lat_lon_box(latitude, longitude, miles)
            params = {'extent': extent}

            response = requests.get(url, headers=self.headers, params=params)

            # Check if the response is successful
            if response.status_code == 200:
                data = response.json()
                if data != {} and data['metadata']['resultset']['count'] > 0:
                    print(f'cleared response: {data}')
                    status = 1
                    continue_loop = 0
                    stations = data['results']
                    min_id = str("")
                    min_distance = miles
                    for station in stations:
                        distance = haversine_spherical_distance((latitude, longitude), (station['latitude'], station['longitude'] ))
                        if distance < min_distance: 
                            min_distance = distance
                            min_id = station['id']


            if status == 0:
                miles += change
                change = change*2
                print(f"Error: {response.status_code}")
                print(response.text)
        return min_id
    
    def date_then(self, time_val):
            # Get today's date
            today = datetime.now()
            
            # Subtract 10 years (approximated as 365.25 days per year to account for leap years)
            then = today - timedelta(days=time_val * 365.25)
            
            # Format the date in ISO format (YYYY-MM-DD)
            return then.strftime('%Y-%m-%d')
    
    def start_end_date(self, time_hold):
        startdate = "&startdate=" + self.date_then(time_hold)
        enddate = "&enddate=" + self.date_then(time_hold-0.5)
        return startdate + enddate
    
    def fetch_weather_data(self, latitude, longitude, time_val):
        min_id = "&stationid=" + self.fetch_station(latitude, longitude)
        endpoint = "/data?"
        results = []
        time_hold = time_val
        for i in range(int((time_val)*2)):
            date_range = self.start_end_date(time_hold)
            time_hold += -0.5
            id = "datasetid=GHCND"
            limit = "&limit=1000"
            units = '&units=standard'

            url = self.base_url + endpoint + id + min_id + date_range + limit + units
            print(url)
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                print(data)
                results_add = data.get("results", [])
                results.extend(results_add)

            time.sleep(1)
        results = pd.DataFrame(data = results)
        return results
