from flask import Flask, render_template
from flask_cors import CORS
from .routes import register_routes
from .database import init_db
from .analyzer import start_analyzer
from .visualizer import start_visualizer
import threading
import sentry_sdk
import os

sentry_sdk.init(
    dsn="https://7407816f67881e03ca804de0a927b74b@o4508440094179328.ingest.us.sentry.io/4508440096079872",
)
port = os.environ.get('PORT', 5000)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def start_consumers():
    # Start the first consumer
    threading.Thread(target=start_analyzer).start()
    # Start the second consumer
    threading.Thread(target=start_visualizer).start()

start_consumers()
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:8000"}})
init_db()
register_routes(app)
import os
from flask import Flask

app = Flask(__name__)

port = os.environ.get('PORT', 5000)  # Default to 5000 if PORT is not set
app.run(host='0.0.0.0', port=port)
    
    
