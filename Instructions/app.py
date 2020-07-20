import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

# reflect
Base.prepare(engine, reflect=True)

# Save
Measurement = Base.classes.measurement
Station = Base.classes.station


#start flask setup
app = Flask(__name__)

#routes
@app.route("/")
def welcome():
    #api routes
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/start-date</br>"
        f"/api/v1.0/start-date/end-date</br>"
        f"start-date & end-date should be formatted as YYYY-MM-DD"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    #create session
    session = Session(engine)

    #query
    results = session.query(Measurement.station, Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()

    session.close()

    #jsonify
    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)



@app.route("/api/v1.0/stations")
def station():
    #create session
    session = Session(engine)

    #query
    results = session.query(Measurement.station).\
        order_by(Measurement.station).all()

    session.close()

    #jsonify
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #create session
    session = Session(engine)

    #query
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(func.strftime("%Y-%m-%d", Measurement.date) >= "2016-08-01", Measurement.station == 'USC00519281').\
    order_by(Measurement.date).all()

    session.close()

    #jsonify
    pop_station_tobs = list(np.ravel(results))

    return jsonify(pop_station_tobs)

@app.route("/api/v1.0/<start>")
def by_start(start):
    #create session
    session = Session(engine)

    #query
    query_date = start

    results = session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(func.strftime("%Y-%m-%d", Measurement.date) >= query_date).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    session.close()

    #jsonify
    user_start_date = list(np.ravel(results))

    return jsonify(user_start_date)

@app.route("/api/v1.0/<start>/<end>")
def by_start_end(start,end):
    #create session
    session = Session(engine)

    #query
    query_start_date = start
    query_end_date = end

    results = session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(func.strftime("%Y-%m-%d", Measurement.date) >= query_start_date).\
    filter(func.strftime("%Y-%m-%d", Measurement.date) <= query_end_date).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    session.close()

    #jsonify
    user_start_date = list(np.ravel(results))

    return jsonify(user_start_date)


#debug
if __name__ == '__main__':
    app.run(debug=True)
