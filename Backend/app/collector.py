
from tasks import send_to_queue
from database import save_weather_data
from workers.fetch_data import fetch_data
from analyzer import start_analyzer

def store_weather_data(lat, lon, years):
    worker = fetch_data()
    print(lat, lon, years)
    weather_data = worker.fetch_weather_data(lat, lon, years)
    print(weather_data)
    if len(weather_data) !=0:
        weather_id = save_weather_data(weather_data)
        send_to_queue('weather_queue', {'weather_id': weather_id})
        return weather_id
    else:
        return None