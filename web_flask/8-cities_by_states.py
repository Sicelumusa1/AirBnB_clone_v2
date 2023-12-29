#!/usr/bin/python3

"""
A script that starts a Flask web application

The web application listens on 0.0.0.0, port 5000

Routes:
        /cities_by_states: display a HTML page with list of 
                     cities per state in the database
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a HTML page with list cities of each state in te database"""
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exception)
    """Remove the current SQLAlchemy Session after each request"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
