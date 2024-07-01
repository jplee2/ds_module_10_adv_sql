# climate_app_Leee

from flask import Flask, jsonify
import pandas as pd
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData, text

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
session = Session(bind=engine)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Q1

app = Flask(__name__)

# Define your routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )




@app.route('/api/v1.0/precipitation')
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    session.close()

    # Create a dictionary with date as the key and prcp as the value
    precipitation_dict = {}
    for date, prcp in results:
        precipitation_dict[date] = prcp

    return jsonify(precipitation_dict)


@app.route('/api/v1.0/stations')
def stations():
    num_stations = session.query(Station.station).all()
    session.close()
    return jsonify(list(np.ravel(num_stations)))
# # Add more routes as needed



@app.route('/api/v1.0/tobs')
def tobs():
    active_station = session.query(Measurement.tobs) \
                 .filter(Measurement.station == 'USC00519281') \
                 .filter(Measurement.date >= dt.datetime.strptime('2016-08-23', '%Y-%m-%d')) \
                 .all()
    session.close()
    return jsonify(list(np.ravel(active_station)))


# @app.route(<start>/<end>)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)







# # Q4
# # Here is a sample code snippet to achieve this:

# # Assuming you have the temperature observations data for the most-active station for the previous year in a variable named `tobs_data`

# # Convert the list of temperature observations to JSON format
# import json
# json_tobs = json.dumps(tobs_data)

# # Print or return the JSON representation
# print(json_tobs)




# # Q5
# # Here is a sample code snippet to achieve this:

# from flask import Flask, jsonify

# # Assuming you have functions to calculate TMIN, TAVG, and TMAX based on the specified date(s)

# app = Flask(__name__)

# @app.route('/api/v1.0/<start>')
# def temperature_start(start):
#     # Calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
#     # Replace these with your actual calculations
#     tmin, tavg, tmax = calculate_temperatures_start(start)
#     return jsonify({'TMIN': tmin, 'TAVG': tavg, 'TMAX': tmax})

# @app.route('/api/v1.0/<start>/<end>')
# def temperature_range(start, end):
#     # Calculate TMIN, TAVG, and TMAX for the dates between start and end dates (inclusive)
#     # Replace these with your actual calculations
#     tmin, tavg, tmax = calculate_temperatures_range(start, end)
#     return jsonify({'TMIN': tmin, 'TAVG': tavg, 'TMAX': tmax})

# if __name__ == '__main__':
#     app.run(debug=True)