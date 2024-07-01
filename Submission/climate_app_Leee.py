from flask import Flask, jsonify
import pandas as pd
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData, text


app = Flask(__name__)


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
session = Session(bind=engine)
Measurement = Base.classes.measurement
Station = Base.classes.station


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

    precipitation_dict = {}
    for date, prcp in results:
        precipitation_dict[date] = prcp

    return jsonify(precipitation_dict)


@app.route('/api/v1.0/stations')
def stations():
    num_stations = session.query(Station.station).all()
    session.close()
    return jsonify(list(np.ravel(num_stations)))




@app.route('/api/v1.0/tobs')
def tobs():
    active_station = session.query(Measurement.tobs) \
                 .filter(Measurement.station == 'USC00519281') \
                 .filter(Measurement.date >= dt.datetime.strptime('2016-08-23', '%Y-%m-%d')) \
                 .all()
    session.close()
    return jsonify(list(np.ravel(active_station)))


@app.route('/api/v1.0/<start>')
def temp_start(start):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)) \
        .filter(Measurement.date >= start_date) \
        .all()
    
    session.close()
    
    temp_stats_dict = {
        "TMIN": temp_stats[0][0],
        "TAVG": temp_stats[0][1],
        "TMAX": temp_stats[0][2]
    }
    
    return jsonify(temp_stats_dict)

@app.route('/api/v1.0/<start>/<end>')
def temp_start_end(start, end):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)) \
        .filter(Measurement.date >= start_date) \
        .filter(Measurement.date <= end_date) \
        .all()
    
    session.close()
    
    temp_stats_dict = {
        "TMIN": temp_stats[0][0],
        "TAVG": temp_stats[0][1],
        "TMAX": temp_stats[0][2]
    }
    
    return jsonify(temp_stats_dict)


if __name__ == '__main__':
    app.run(debug=True)


