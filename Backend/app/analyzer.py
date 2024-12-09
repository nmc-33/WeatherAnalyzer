from tasks import start_consumer, send_to_queue
import json
from database import get_weather_data_by_id, save_processed_weather_data
from workers.data_analyzer import perform_analysis
from visualizer import start_visualizer

def analyze_callback(ch, method, properties, body):
    print('pulled from weather_queue')
    weather_id = json.loads(body)['weather_id']
    print('got id')
    data = get_weather_data_by_id(weather_id)
    if data:
        print
        ch.basic_ack(delivery_tag=method.delivery_tag)
        result = perform_analysis(data)
        processed_id = save_processed_weather_data(result)
        send_to_queue('processed_queue', {'processed_id': processed_id, 'weather_id': weather_id})
        print('sent to processed_queue')


def analyze_callback_test(weather_id):
    data = get_weather_data_by_id(weather_id)
    if data:
        result = perform_analysis(data)
        save_processed_weather_data(result)

def start_analyzer():
    start_consumer('weather_queue', analyze_callback)