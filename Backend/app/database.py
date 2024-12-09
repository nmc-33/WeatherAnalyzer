from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text
import json

Base = declarative_base()

class HTMLData(Base):
    __tablename__ = 'html_data'
    id = Column(Integer, primary_key=True) 
    content = Column(Text, nullable=False)

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    date = Column(Text)
    datatype = Column(Text)
    station = Column(Text)
    attributes = Column(Text)
    value = Column(Text)

class ProcessedWeatherData(Base):
    __tablename__ = 'processed_weather_data'
    id = Column(Integer, primary_key=True)
    total_snow_yearly = Column(Text)
    average_low = Column(Text)
    average_high = Column(Text)
    average_temp = Column(Text)
    total_snow_month = Column(Text)
    avg_snow_depth = Column(Text)
    years = Column(Text)
    months = Column(Text)
    year_month = Column(Text)
    month_year = Column(Text)


# Database connection string (SQLite for this example)
DATABASE_URL = 'sqlite:///weather.db'

# Create engine and sessionmaker
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Function to initialize the database (create tables)
def init_db():
    """
    Create tables in the database if they don't already exist.
    """
    Base.metadata.create_all(engine)
    print("Database initialized and tables created.")

# Function to save weather data (raw data)
def save_weather_data(weather_data):
    """
    Save raw weather data to the database.
    Returns the ID of the newly inserted record.
    """
    try:
        with Session() as session:
            print(weather_data)
            new_entry = WeatherData(
                date=json.dumps(weather_data['date'].tolist()),
                datatype=json.dumps(weather_data['datatype'].tolist()),
                station=json.dumps(weather_data['station'].tolist()),
                attributes=json.dumps(weather_data['attributes'].tolist()),
                value=json.dumps(weather_data['value'].tolist())
            )
            session.add(new_entry)
            session.commit()
            print(f"Saved weather data with ID: {new_entry.id}")
            return new_entry.id
    except Exception as e:
        print(weather_data)
        print(f"Error saving weather data: {e}")
        return None

# Function to save processed weather data
def save_processed_weather_data(processed_data):
    """
    Save processed weather data to the database.
    Returns the ID of the newly inserted record.
    """
    try:
        with Session() as session:
            new_processed_entry = ProcessedWeatherData(
                total_snow_yearly = json.dumps(processed_data['total_snow_yearly']),
                average_low=json.dumps(processed_data['average_low']),
                average_high=json.dumps(processed_data['average_high']),
                average_temp=json.dumps(processed_data['average_temp']),
                total_snow_month=json.dumps(processed_data['total_snow_month']),
                avg_snow_depth=json.dumps(processed_data['avg_snow_depth']),
                years = json.dumps(processed_data['years']),
                months = json.dumps(processed_data['month']),
                year_month = json.dumps(processed_data['year_month']),
                month_year = json.dumps(processed_data['month_year']),
            )
            session.add(new_processed_entry)
            session.commit()
            print(f"Saved processed data with ID: {new_processed_entry.id}")
            return new_processed_entry.id
    except Exception as e:
        print(f"Error saving processed weather data: {e}")
        return None

def save_html_data(html_data, weather_id):
    """
    Save HTML data to the database.
    Returns the ID of the newly inserted record.
    """
    try:
        with Session() as session:
            # Create a new HtmlData entry
            new_html_entry = HTMLData(
                id = weather_id,
                content=json.dumps(html_data)    # Extract the content from the dictionary
            )
            
            # Add the entry to the session and commit the transaction
            session.add(new_html_entry)
            session.commit()
            
            # Print success message and return the ID of the new record
            print(f"Saved HTML data with ID: {new_html_entry.id}")
            return new_html_entry.id
    except Exception as e:
        # Print error message if there was an issue
        print(f"Error saving HTML data: {e}")
        return None

# Function to retrieve weather data by ID (raw)
def get_weather_data_by_id(weather_id):
    """
    Retrieve raw weather data from the database by ID.
    """
    try:
        with Session() as session:
            weather_data = session.query(WeatherData).filter(WeatherData.id == weather_id).first()
            if weather_data:
                return {
                    "id": weather_data.id,
                    "date": json.loads(weather_data.date),
                    "datatype": json.loads(weather_data.datatype),
                    "station": json.loads(weather_data.station),
                    "attributes": json.loads(weather_data.attributes),
                    "values": json.loads(weather_data.value)
                }
            else:
                print(f"Weather data with ID {weather_id} not found.")
                return None
    except Exception as e:
        print(f"Error retrieving weather data: {e}")
        return None

# Function to retrieve processed weather data by ID
def get_processed_weather_data_by_id(processed_id):
    """
    Retrieve processed weather data from the database by ID.
    """
    try:
        with Session() as session:
            processed_data = session.query(ProcessedWeatherData).filter(ProcessedWeatherData.id == processed_id).first()
            if processed_data:
                return {
                    "total_snow_yearly": json.loads(processed_data.total_snow_yearly),
                    "average_low": json.loads(processed_data.average_low),
                    "average_high": json.loads(processed_data.average_high),
                    "average_temp": json.loads(processed_data.average_temp),
                    "total_snow_month": json.loads(processed_data.total_snow_month),
                    "avg_snow_depth": json.loads(processed_data.avg_snow_depth),
                    "years": json.loads(processed_data.years),
                    "months": json.loads(processed_data.months),
                    "year_month": json.loads(processed_data.year_month),
                    "month_year": json.loads(processed_data.month_year),
                }
            else:
                print(f"Processed weather data with ID {processed_id} not found.")
                return None
    except Exception as e:
        print(f"Error retrieving processed weather data: {e}")
        return None

def get_html_data_by_id(weather_id):
    """
    Retrieve processed weather data from the database by ID.
    """
    try:
        with Session() as session:
            html_data = session.query(HTMLData).filter(HTMLData.id == weather_id).first()
            if html_data:
                return json.loads(html_data.content)
            else:
                return None
    except Exception as e:
        print(f"Error retrieving html weather data: {e}")
        return None

# Example usage (optional)
if __name__ == "__main__":
    # Initialize the database and create tables
    init_db()

    # Example: Save raw weather data (you'd replace this with actual data)
    weather_data = {
        "date": "2024-12-08",
        "datatype": "TMAX",
        "station": "Station-01",
        "attributes": "Temperature",
        "value": 10.5
    }
    weather_id = save_weather_data(weather_data)

    # Example: Retrieve raw weather data by ID
    if weather_id:
        raw_data = get_weather_data_by_id(weather_id)
        print("Raw weather data:", raw_data)

    # Example: Save processed weather data
    processed_data = {
        "total_snow_yearly": 100.0,
        "average_low": -5.2,
        "average_high": 12.3,
        "average_temp": 3.4,
        "total_snow_month": 20.0,
        "avg_snow_depth": 5.0
    }
    processed_id = save_processed_weather_data(processed_data)
    print(f"Processed data saved with ID: {processed_id}")