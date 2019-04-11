import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()

last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
for date in last_date:
    last_date_list=date

last_date_obj=dt.datetime.strptime(last_date_list, '%Y-%m-%d')
first_date=last_date_obj - dt.timedelta(days=365)

def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
def calc_temp_start(start_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
#Flask Setup
app = Flask(__name__)

#Flask Routes
@app.route("/")
def welcome( ):
    """List of all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/start_date</br>"
        f"/api/v1.0/start/end</br>"
    )

@app.route("/api/v1.0/precipitation")
def precip( ):
    """Return Precipitation Data."""
    results=session.query(Measurement.date,Measurement.prcp).all()
    precip_date=list(np.ravel(results))
    return (jsonify(precip_date))

@app.route("/api/v1.0/stations")
def stations( ):
    """Return List of Stations."""
    #Update this
    result=session.query(Measurement.station).group_by(Measurement.station).all()
    station_list=list(np.ravel(result))
    return (jsonify(station_list))

@app.route("/api/v1.0/tobs")
def tobs( ):
    """Return List of Temperature Obs. Data."""
    
    last_year_temp=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>=first_date).all()
    table_last_temp=list(np.ravel(last_year_temp))
    return (jsonify(table_last_temp))

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    """Return List of Temperature Obs. Data with start date."""
    
    return (jsonify(calc_temp_start(start_date)))
    
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    """Return List of Temperature Obs. Data with start and end date."""
    
    return (jsonify(calc_temps(start, end))

    )
if __name__ == '__main__':
    app.run(debug=True)