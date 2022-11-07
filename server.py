
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import journey
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, session

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
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
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
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/2.0.x/api/?highlight=incoming%20request%20data

  """

  # DEBUG: this is debugging code to see what request looks like
  print("request", request.args)

  # if the request sorted


  #
  # DATABASE QUERIES
  #

  query = "SELECT C.name, J.start_station_name, J.end_station_name, J.identifier, J.rating, J.date \
    FROM Commuter C, Journey J \
    WHERE C.ssn = J.ssn"

  # Get Journey
  if ("filter" in session and session["filter"] == "sort"):
    query = "SELECT C.name, J.start_station_name, J.end_station_name, J.identifier, J.rating, J.date \
    FROM Commuter C, Journey J \
    WHERE C.ssn = J.ssn\
    ORDER BY J.date"

  if ("rating" in session and session["rating"] != "default"):
    query = "SELECT C.name, J.start_station_name, J.end_station_name, J.identifier, J.rating, J.date \
    FROM Commuter C, Journey J \
    WHERE C.ssn = J.ssn AND J.rating >= {}".format(session["rating"])

  print(query)
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

  session["filter"] = "default"
  session["rating"] = "default"

  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #
  #     # creates a <div> tag for each element in data
  #     # will print:
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = journeys)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")


@app.route('/post-journey')
def postJourney():

  # Gets all subway line identifiers
  cursor = g.conn.execute("SELECT DISTINCT L.identifier FROM Line L")
  identifiers = []
  for result in cursor:
    identifiers.append(result)
  cursor.close()

  context = dict(data = identifiers)

  return render_template("postJourney.html", **context)

# Example of adding new data to the database
@app.route('/sort', methods=['GET'])
def sort():
  session["filter"] = "sort"
  return redirect('/')

@app.route('/rating', methods=['GET'])
def route():
  session["rating"] = request.args['num']
  return redirect('/')

@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')

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
  is_cs_student = request.form['is_cs_student']

  cursor = g.conn.execute('SELECT * FROM Commuter C WHERE C.ssn = %s', ssn)

  commuter_exists = False
  for result in cursor:
    commuter_exists = True

  if not commuter_exists:
    g.conn.execute('INSERT INTO Commuter VALUES (%s, %s, %s, %s);', ssn, name, age, is_cs_student)

  #ssn, identifier, train_id, start_station, end_station, rating, date = request.form['ssn', 'identifier', 'train_id', 'start_station', 'end_station', 'rating', 'date']
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
