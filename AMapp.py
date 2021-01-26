# `/api/v1.0/precipitation`
  # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
  # Return the JSON representation of your dictionary.
# `/api/v1.0/stations`
  # Return a JSON list of stations from the dataset.
# `/api/v1.0/tobs`
  # Query the dates and temperature observations of the most active station for the last year of data.
  # Return a JSON list of temperature observations (TOBS) for the previous year.
# `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
  # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
  # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
  # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

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
    f"/api/v1.0/<start><br/>"
    f"/api/v1.0/<start>/<end><br/>"
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

if __name__ == "__main__":
    app.run(debug=True)
