
"""
Columbia's COMS W4111.001 Introduction to Databases
JourneyJournal by Uma Bahl and Abram Kremer
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
"""
import journey
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, session
import regex as re
import json
import random

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# Connects to our database.
#
DATABASEURI = "postgresql://ank2177:8575@34.75.94.195/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Sets up the application to use cookies.
#
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
@app.route('/')
def index():
  #
  # DATABASE QUERIES
  #

  # Gets all the Journeys.
  query = "SELECT C.name, J.start_station_name, J.end_station_name, J.identifier, J.rating, J.date \
    FROM Commuter C, Journey J \
    WHERE C.ssn = J.ssn"

  # Get Journeys, ordered.
  if ("filter" in session and session["filter"] == "sort"):
    query = "SELECT C.name, J.start_station_name, J.end_station_name, J.identifier, J.rating, J.date \
    FROM Commuter C, Journey J \
    WHERE C.ssn = J.ssn\
    ORDER BY J.date"

  # Gets Journeys for a specific rating.
  if ("rating" in session and session["rating"] != "default"):
    query = "SELECT C.name, J.start_station_name, J.end_station_name, J.identifier, J.rating, J.date \
    FROM Commuter C, Journey J \
    WHERE C.ssn = J.ssn AND J.rating >= {}".format(session["rating"])

  # Executes the Query.
  cursor = g.conn.execute(query)
  journeys = []
  for result in cursor:
  	new_journey = journey.Journey(
      result['name'],
  		result['start_station_name'],
  		result['end_station_name'],
  		result['identifier'],
  		result['rating'],
  		result['date']
  	)
  	journeys.append(new_journey)

  # Refreshes any filters.
  session["filter"] = "default"
  session["rating"] = "default"

  cursor.close()

  #
  # Variables passed to the Jinja template.
  #
  context = dict(data = journeys)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# PATHS
#
@app.route('/post-journey')
def postJourney():
  # Gets all subway line identifiers.
  cursor = g.conn.execute("SELECT DISTINCT L.identifier FROM Line L")
  identifiers = []
  for result in cursor:
    identifiers.append(result)
  cursor.close()

  context = dict(data = identifiers)

  return render_template("postJourney.html", **context)

# Filters for getting Journey information.
@app.route('/sort', methods=['GET'])
def sort():
  session["filter"] = "sort"
  return redirect('/')

@app.route('/rating', methods=['GET'])
def route():
  session["rating"] = request.args['num']
  return redirect('/')

# Recieves a station name.
# Retrieves the rats at that station along with their favorite food.
@app.route('/rat', methods=["GET"])
def rat():
	station = request.args["station"].strip()

	query = "SELECT R.name, R.sname, R.favorite_food \
	FROM Rat_Lives_At R \
	WHERE R.sname ~ '\y{}\y';".format(station)

	cursor = g.conn.execute(query)
	results = []

	for result in cursor:
		results.append({
			"name": result[0],
			"sname": result[1],
			"food": result[2]
		})

	if (len(results) > 0):
		return json.dumps({"rat": random.choice(results)})
	else:
		return json.dumps({"rat": {
			"name": "No Ratz",
			"sname": "No Ratz",
			"food": "No Ratz"
		}})

# POST endpoint for inserting new Journey tuple
@app.route('/insert-new-journey', methods=['POST'])
def insertNewJourney():
  ssn = request.form['ssn']
  identifier = request.form['identifier']
  start_station = request.form['start_station']
  end_station = request.form['end_station']
  train_id = request.form['train_id']
  rating = request.form['rating']
  date = request.form['date']
  name = request.form['name']
  age = request.form['age']
  try:
    is_cs_student = request.form['is_cs_student']
  except:
    is_cs_student = False

  # INPUT VERIFICATION (to prevent SQL injections / errors)
  # If it fails any, the query is not executed and the user is brought back to the home page.
  # Make sure ssn is a 9 digit number.
  if (len(ssn) != 9 or not re.search('^[0-9]*$', ssn)):
  	print("Invalid ssn")
  	return redirect('/')

  # Make sure identifier is valid.
  if (len(identifier) > 1):
  	print("Invalid identifier")
  	return redirect('/')

  # Make sure start station and end station are alphanumeric (can include the - symbol).
  if (not re.search('^[-a-zA-Z0-9 ]*$', start_station) or not re.search('^[-a-zA-Z0-9 ]*$', end_station)):
  	print("Invalid station name")
  	return redirect('/')

  # Make sure train_id is valid.
  if (len(train_id) != 10 or not re.search('^[0-9]*$', train_id)):
  	print("Invalid train id")
  	return redirect('/')

  # Make sure rating is between 1 - 5.
  if (not re.search('^[1-5]$', rating)):
  	print("Invalid rating")
  	return redirect('/')

  # Make sure the date is valid mm/dd/yyyy.
  if (not re.search('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', date)):
  	print("Invalid date")
  	return redirect('/')

  # Make sure name is alphanumeric (can include the - symbol).
  if (not re.search('^[-a-zA-Z0-9 ]*$', name)):
  	print("Invalid name")
  	return redirect('/')

  # Make sure age is valid.
  if (not re.search('^[0-9]*$', age)):
  	print("Invalid age")
  	return redirect('/')

  cursor = g.conn.execute('SELECT * FROM Commuter C WHERE C.ssn = %s', ssn)

  commuter_exists = False
  for result in cursor:
    commuter_exists = True

  if not commuter_exists:
    g.conn.execute('INSERT INTO Commuter VALUES (%s, %s, %s, %s);', ssn, name, age, is_cs_student)

  g.conn.execute('INSERT INTO Journey VALUES (%s, %s, %s, %s, %s, %s, %s);', train_id, start_station, end_station, ssn, identifier, rating, date)
  return redirect('/')


@app.route('/get-start-stations')
def getStartStations():
  identifier = request.args["identifier"]
  
  cursor = g.conn.execute('SELECT DISTINCT SA.name FROM Services S, Stops_At SA WHERE S.train_id = SA.train_id AND S.identifier = %s', identifier)
  start_stations = []
  for result in cursor:
    start_stations.append(result["name"])
  cursor.close()
  
  return start_stations

@app.route('/view-commuters')
def viewCommuters():
  
  cursor = g.conn.execute('SELECT DISTINCT * FROM Commuter C')
  commuters = []
  for result in cursor:
    commuters.append((result["name"].strip(), result["age"], result["ssn"], result["is_cs_student"]))
  cursor.close()
  
  return commuters

@app.route('/view-journeys')
def viewJourneys():
  
  cursor = g.conn.execute('SELECT DISTINCT * FROM Journey J')
  commuters = []
  for result in cursor:
    commuters.append((result["ssn"]))
  cursor.close()
  
  return commuters

@app.route('/get-end-stations')
def getEndStations():
  identifier = request.args["identifier"]
  start_station = request.args["start_station"]
  
  cursor = g.conn.execute('SELECT DISTINCT SA.name FROM Services S, Stops_At SA WHERE S.train_id = SA.train_id AND S.identifier = %s AND SA.name != %s', identifier, start_station)
  end_stations = []
  for result in cursor:
    end_stations.append(result["name"])
  cursor.close()
  
  return end_stations

@app.route('/get-trains')
def getTrains():
  identifier = request.args["identifier"]
  start_station = request.args["start_station"]
  end_station = request.args["end_station"]
  
  cursor = g.conn.execute('SELECT DISTINCT SA.train_id FROM Services S, Stops_At SA, Stops_At SA2 WHERE S.train_id = SA.train_id AND S.train_id = SA2.train_id AND S.identifier = %s AND SA.name != %s AND SA2.name != %s', identifier, start_station, end_station)
  train_ids = []
  for result in cursor:
    train_ids.append(result["train_id"])
  cursor.close()
  
  return train_ids

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
