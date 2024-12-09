from flask import Blueprint, request, jsonify
from .collector import store_weather_data
from .database import get_html_data_by_id


api = Blueprint('api', __name__)

@api.route('/weather', methods=['POST'])
def submit_weather_data():
    data = request.json
    # Assume data includes 'lat' and 'lon'
    lat = data.get('lat')
    lon = data.get('lon')
    year = data.get('year')
    if not lat or not lon or year > 50 or lat > 180 or lat < -180 or lon > 180 or lon < -180:
        return jsonify({"error": "Latitude, Longitude are required. Historical Years must be <50."}), 400

    # Simulate storing weather data and sending to RabbitMQ
    weather_id = store_weather_data(lat, lon, year)  # Function from `collector.py`
    if weather_id:
        return jsonify({"message": "Weather data submitted", "weather_id": weather_id}), 200
    else:
        return jsonify({"message": "No data available for that location"})

# @api.route('/weather/<int:weather_id>', methods=['GET'])
# def get_raw_weather_data(weather_id):
#     data = get_weather_data_by_id(weather_id)  # From `database.py`
#     if not data:
#         return jsonify({"error": "Weather data not found"}), 404
#     return jsonify(data), 200

# @api.route('/analysis/<int:processed_id>', methods=['GET'])
# def get_analysis(processed_id):
#     data = get_processed_weather_data_by_id(processed_id)  # From `database.py`
#     if not data:
#         return jsonify({"error": "Processed data not found"}), 404
#     return jsonify(data), 200

# @api.route('/analyze/<int:weather_id>', methods=['POST'])
# def trigger_analysis(weather_id):
#     send_to_queue('weather_queue', {'weather_id': weather_id})
#     return jsonify({"message": "Analysis triggered"}), 200

@api.route('/heath', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@api.route('/visualize/<int:weather_id>', methods=['GET'])

def register_routes(app):
    app.register_blueprint(api, url_prefix="/api")