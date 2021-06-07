# Import everything you used in the starter_climate_analysis.ipynb file, along with Flask modules
from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from datetime import date
import sqlite3

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# Create an engine
engine = create_engine(f"sqlite:///data/hawaii.sqlite")
# reflect an existing database into a new model with automap_base() and Base.prepare()
Base = automap_base()
# Save references to each table
Base.prepare(engine, reflect = True)

# Instantiate a Session and bind it to the engine
HawaiiMeasurement = Base.classes.measurement
HawaiiStation = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
# Instantiate a Flask object at __name__, and save it to a variable called app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Set the app.route() decorator for the base '/'
@app.route("/")
# define a welcome() function that returns a multiline string message to anyone who visits the route
def welcome():
    print("Server is working. Server received request for Welcome Page")
    return (
        f"You made it the SQLAlchemy Project Surf's Up!<br/>"
        # f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

# Set the app.route() decorator for the "/api/v1.0/precipitation" route
@app.route("/api/v1.0/precipitation")
# define a precipitation() function that returns jsonified precipitation data from the database
def precipitation():
    print("Server is working. Server received request for Precipitation Page")
# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    # Calculate the date 1 year ago from last date in database
    last_year = dt.date(2017, 8, 23) - timedelta(days = 365)
    # Query for the date and precipitation for the last year
    results = session.query(HawaiiMeasurement.date, HawaiiMeasurement.prcp).\
    filter(HawaiiMeasurement.date >= last_year).all()
    # Create a dictionary to store the date: prcp pairs. 
    prcp_pairs = {date: prcp for date, prcp in precipitation}
    # Hint: check out a dictionary comprehension, which is similar to a list comprehension but allows you to create dictionaries
    
    # Return the jsonify() representation of the dictionary
    return jsonify(prcp_pairs)
    
# Set the app.route() decorator for the "/api/v1.0/stations" route
@app.route("/api/v1.0/stations")
# define a stations() function that returns jsonified station data from the database
def stations():
    print("Server is working. Server received request for Stations Page")
# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    # Query for the list of stations
    results = session.query(HawaiiStation.station).all()
    # Unravel results into a 1D array and convert to a list
    # Hint: checkout the np.ravel() function to make it easier to convert to a list
    stations = list(np.ravel(results))
    # Return the jsonify() representation of the list
    return jsonify(stations=stations)

# Set the app.route() decorator for the "/api/v1.0/tobs" route
@app.route("/api/v1.0/tobs")
# define a temp_monthly() function that returns jsonified temperature observations (tobs) data from the database
def temp_monthly():
    print("Server is working. Server received request for Monthly Temp Page")
# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    # Calculate the date 1 year ago from last date in database
    last_year = dt.date(2017, 8, 23) - timedelta(days = 365)
    # Query the primary station for all tobs from the last year
    results = session.query(HawaiiMeasurement.tobs).\
        filter(HawaiiMeasurement.station == 'USC00519281').\
        filter(HawaiiMeasurement.date >= last_year).all()
    # Unravel results into a 1D array and convert to a list
    # Hint: checkout the np.ravel() function to make it easier to convert to a list
    temps = list(np.ravel(results))
    # Return the jsonify() representation of the list
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run(debug=True)
