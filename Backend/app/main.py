from flask import Flask
from flask_cors import CORS
from routes import register_routes
from database import init_db
from analyzer import start_analyzer
from visualizer import start_visualizer
import threading
import sentry_sdk

# db = SQLAlchemy()
# migrate = Migrate()

def start_consumers():
    # Start the first consumer
    threading.Thread(target=start_analyzer).start()
    # Start the second consumer
    threading.Thread(target=start_visualizer).start()

def create_app():
    app = Flask(__name__)
    CORS(app)

    init_db()

    # # Load configuration from environment or default to production settings
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost:5432/weather_db')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional to disable tracking modifications

    # # Initialize database and migrate
    # db.init_app(app)
    # migrate.init_app(app, db)

    # Register routes (assuming you have a separate module for routes)
    register_routes(app)

    return app

if __name__ == "__main__":
    sentry_sdk.init(
        dsn="https://7407816f67881e03ca804de0a927b74b@o4508440094179328.ingest.us.sentry.io/4508440096079872",
    )
    start_consumers()
    app = create_app()
    app.run()
    