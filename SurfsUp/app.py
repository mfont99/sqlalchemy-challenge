# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Home page!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (YYYY-MM-DD)<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    most_recent = session.query(func.max(measurement.date)).scalar()

    current_date = dt.datetime.strptime(most_recent, '%Y-%m-%d')
    one_year_ago = current_date - dt.timedelta(days=365)

    precipitation_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago).all()

    precip_df = pd.DataFrame(precipitation_data, columns=['date', 'prcp'])

    sorted_df = precip_df.sort_values(by='date')

    prcp_analysis = sorted_df.set_index('date')['prcp'].to_dict()

    return jsonify(prcp_analysis)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    stations_list = list(np.ravel(stations))
    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    most_active_station = stations[0][0]

    most_recent = session.query(func.max(measurement.date)).scalar()
    current_date = dt.datetime.strptime(most_recent, '%Y-%m-%d')
    one_year_ago = current_date - dt.timedelta(days=365)

    temps = session.query(measurement.tobs).filter(measurement.station == most_active_station).filter(measurement.date >= one_year_ago).all()
    temps_list = list(np.ravel(temps))

    return jsonify(temps_list)

@app.route("/api/v1.0/<start_date>")        # Use YYYY-MM-DD format and only input data
def start_date(start_date):                 # that exists in the .csv file
    session = Session(engine)

    temp_data = session.query(measurement.tobs).filter(measurement.date >= start_date).all()
    raw_numbers = [val[0] for val in temp_data]
    
    min_value = min(raw_numbers)
    max_value = max(raw_numbers)
    avg_value = sum(raw_numbers) / len(raw_numbers)

    dict = {
        "min_value": min_value,
        "max_value": max_value,
        "avg_value": avg_value
    }

    return jsonify(dict)

@app.route("/api/v1.0/<start_date>/<end_date>")     # Same info as the above route
def start_date_end_date(start_date, end_date):
    session = Session(engine)

    temp_data = session.query(measurement.tobs).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    raw_numbers = [val[0] for val in temp_data]

    min_value = min(raw_numbers)
    max_value = max(raw_numbers)
    avg_value = sum(raw_numbers) / len(raw_numbers)

    dict = {
        "min_value": min_value,
        "max_value": max_value,
        "avg_value": avg_value
    }

    return jsonify(dict)

if __name__ == "__main__":
    app.run(debug=True)