from flask import Flask, render_template
from flask_cors import CORS
from .routes import register_routes
from .database import init_db
from .analyzer import start_analyzer
from .visualizer import start_visualizer
import threading
import sentry_sdk

sentry_sdk.init(
    dsn="https://7407816f67881e03ca804de0a927b74b@o4508440094179328.ingest.us.sentry.io/4508440096079872",
)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def start_consumers():
    # Start the first consumer
    threading.Thread(target=start_analyzer).start()
    # Start the second consumer
    threading.Thread(target=start_visualizer).start()



if __name__ == "__main__":
    start_consumers()
    CORS(app)
    init_db()
    register_routes(app)
    app.run()
    