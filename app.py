########################
#Import Dependencies
########################
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

#Import Flask and jsonify
#Flask will be used to create the server and jsonify will convert query results to json
from flask import Flask, jsonify

##############################################
#Create Engine, automap, save table references
##############################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

########################################
#Setup Flask
########################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the SQL-Alchemy APP API - SURFS UP!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-24").\
    filter(Measurement.date <= "2017-08-23").all()

     # Convert the list to Dictionary
    all_prcp = {}
    for date,prcp  in precipitation_data:
        all_prcp["date"] = date
        all_prcp["prcp"] = prcp
               
    return jsonify(all_prcp)
    
    session.close()

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    stations_active = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    # Create a list of stations ids
    stations_ids = []
    for station_active in stations_active:
        station = station_active[0]
        stations_ids.append(station)
    
    # Return a JSON list from the dataset
    stations = {}
    stations['stations'] = stations_ids
               
    return jsonify(stations)

    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
    stations_active = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    
    # Find most active station
    station_most_active=stations_active[0][0]
    
    # Dine Weather for Most Active Station
    weather = session.query(func.min(Measurement.tobs),\
    func.max(Measurement.tobs),\
    func.avg(Measurement.tobs)).filter(Measurement.station == station_most_active).all()

    # Convert tuple to a list
    weather_list = list(weather[0])
     
    # Return a JSON list from the dataset
    station_weather = {}
    station_weather['weather'] = weather_list
               
    return jsonify(station_weather)
    
    session.close()


   

if __name__ == '__main__':
    app.run(debug=True)

    
