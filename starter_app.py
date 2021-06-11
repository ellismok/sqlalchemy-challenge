### IMPORT LIBRARIES ###
from matplotlib import style
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from pandas.plotting import table

from datetime import datetime, timedelta
from datetime import date

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

from flask import Flask, jsonify


### DATABASE SET UP ###

# Create an engine
engine = create_engine("sqlite:///data/hawaii.sqlite")
# Use automap_base() to reflect the existing table and using .prepare() to reflect the schema and produce mapping
Base = automap_base()
# Save references to each table
Base.prepare(engine, reflect = True)
# Create a session
session = Session(engine)
# Create mapped classes with new variable names 
HawaiiMeasurement = Base.classes.measurement
HawaiiStation = Base.classes.station


### FLASK SET UP ###
app = Flask(__name__)


### ROUTE SET UP ###
@app.route("/")
def homepage():
    return (
        f"You made it the SQLAlchemy Project: Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/precipitation<br/>"
        f"/stations<br/>"
        f"/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )  


@app.route("/precipitation")
def precipitation():
    # Create a session
    session = Session(engine)   
    print("Server is working. Server received request for Precipitation Page")
    # Calculate the date 1 year ago from last date in database
    last_data_point = (session.query(HawaiiMeasurement.date)
    .order_by(HawaiiMeasurement.date.desc())
    .all())[0]
    # Query for the date and precipitation for the last year
    last_data = date.fromisoformat('2017-08-23')
    last_year = last_data - timedelta(days = 365)

    # List of precipitation the past year
    one_year_prcp = (session
    .query(HawaiiMeasurement.date, HawaiiMeasurement.prcp)
    .filter(HawaiiMeasurement.date >= last_year)
    .all())

    session.close()
    # Use a shortcut for loop and use it to convert a list to dict by using `date` = key & `prcp` = value
    convert_dict = {date: prcp for date, prcp in one_year_prcp}
    # Return the jsonify() representation of the dictionary
    return jsonify(convert_dict)
    # SUB: return "json of dictionary using jsonify(dict_name)"
    

@app.route("/stations")
def stations():
    # Create a session
    session = Session(engine) 
    print("Server is working. Server received request for Stations Page")
    # Query for the list of stations
    total_number_of_stations = (session.query(HawaiiStation.station).all())

    session.close()
    # numpy.ravel() function returns contiguous flattened array
    stations_list = list(np.ravel(total_number_of_stations))
    return jsonify(stations_list=stations_list)
    # SUB: return "json of dictionary using jsonify(dict_name)"


@app.route("/tobs")
def tobs():
    # Create a session
    session = Session(engine) 
    print("Server is working. Server received request for TOB Page")
    # Calculate the date 1 year ago from last date in database
    last_data = date.fromisoformat('2017-08-23')
    last_year = last_data - timedelta(days = 365)
    # Query the dates and temperature observations of the most active station for the last year of data.
    active_stat = (session
                    .query(HawaiiMeasurement.station,
                    func.avg(HawaiiMeasurement.tobs)
                    , func.max(HawaiiMeasurement.tobs)
                    , func.min(HawaiiMeasurement.tobs))
                    .filter(HawaiiMeasurement.station == 'USC00519281')
                    .all())
    # # Query the primary station for all tobs from the last year
    highest_tob = (session
               .query(HawaiiMeasurement.date
                , HawaiiMeasurement.station
                , HawaiiMeasurement.tobs)
               .filter(HawaiiMeasurement.station == 'USC00519281')
               .filter(HawaiiMeasurement.date >= last_year)
               .all())
    session.close()
    tobs = list(np.ravel(highest_tob))
    return jsonify(tobs=tobs)
    # SUB: return "json of dictionary using jsonify(dict_name)"


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def summary(start=None, end=None):
    # Create a session
    session = Session(engine) 
    
    # Select statement
    sel = [func.min(HawaiiMeasurement.tobs), func.avg(HawaiiMeasurement.tobs), func.max(HawaiiMeasurement.tobs)]

    #  Given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
    if not end: 
        dates_greater = (session
                .query(func.min(HawaiiMeasurement.tobs)
                , func.avg(HawaiiMeasurement.tobs)
                , func.max(HawaiiMeasurement.tobs))
                .filter(HawaiiMeasurement.date >= start)
                .all())
        return jsonify(summary=dates_greater)

    dates_greater = (session
                .query(func.min(HawaiiMeasurement.tobs)
                , func.avg(HawaiiMeasurement.tobs)
                , func.max(HawaiiMeasurement.tobs))
                .filter(HawaiiMeasurement.date >= start)
                .filter(HawaiiMeasurement.date <= end)
                .all())
    session.close()
    return jsonify(summary=dates_greater)

if __name__ == '__main__':
    app.run(debug=True)
