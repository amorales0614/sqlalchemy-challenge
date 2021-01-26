#import same dependencies from pandas script
import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)

# Save references to each table
msmt = Base.classes.measurement
station = Base.classes.station

#begin setting up flask
app = Flask(__name__)

##start setting up routes

#list all available routes
@app.route("/")
def homepage():
  return (
    f"Welcome! Here are your available routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/yyyy-mm-dd (uses a start date)<br/>"
    f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd (uses a start and end date"
    )

@app.route("/api/v1.0/precipitation")
def precip():
	session = Session(engine)

	results = session.query(msmt.date, msmt.prcp).order_by(msmt.date).all()

	pd_list = []

	for date, prcp in results:
		pd_dict = {}
		pd_dict[date] = prcp
		pd_list.append(pd_dict)

	session.close()

	return jsonify(pd_list)

@app.route("/api/v1.0/stations")
def stations():
	session = Session(engine)

	stns = {}

	results = session.query(station.station, station.name).all()

	for s_id, name in results:
		stns[s_id] = name

	session.close()

	return jsonify(stns)

@app.route("/api/v1.0/tobs")
def tobs():
	session = Session(engine)

	most_recent = session.query(msmt.date).order_by(msmt.date.desc()).first()

	first_date = (dt.datetime.strptime(most_recent[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')

	results = session.query(msmt.date, msmt.tobs).filter(msmt.date >= first_date).order_by(msmt.date).filter(msmt.station == 'USC00519281').all()

	t_list = []

	for date, temp in results:
		t_dict = {}
		t_dict[date] = temp
		t_list.append(t_dict)

	session.close()

	return jsonify(t_list)

@app.route("/api/v1.0/<start>")
def f_start(start):

	session = Session(engine)

	start_list = [] 

	results = session.query(func.min(msmt.tobs), func.max(msmt.tobs), func.avg(msmt.tobs)).filter(msmt.date >= start).all()

	for min, max, avg in results:
		start_dict = {}
		start_dict["TMIN"] = min
		start_dict["TMAX"] = max
		start_dict["TAVG"] = avg
		start_list.append(start_dict)

	session.close()

	return jsonify(start_dict)

  # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
def f_startend(start,end):

	session = Session(engine)

	startend_list = [] 

	results = session.query(func.min(msmt.tobs), func.max(msmt.tobs), func.avg(msmt.tobs)).filter(msmt.date >= start).filter(msmt.date <= end).all()

	for min, max, avg in results:
		startend_dict = {}
		startend_dict["TMIN"] = min
		startend_dict["TMAX"] = max
		startend_dict["TAVG"] = avg
		startend_list.append(startend_dict)

	session.close()

	return jsonify(startend_dict)

if __name__ == "__main__":
    app.run(debug=True)
