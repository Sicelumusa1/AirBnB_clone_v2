#!/usr/bin/python3

"""
A script that starts a Flask web application

The web application listens on 0.0.0.0, port 5000

Routes:
        /states: display a HTML page with list of states
        /states/<id>: display a HTML page with list of cities per state
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def show_states():
    """Display a HTML page with list of  state in te database"""
    states = storage.all("State")
    return render_template("9-states.html", states=states, stateId=None)


@app.route('/states/<id>', strict_slashes=False)
def cities_of_states(id):
    """
    Display a HTML page with list cities of each state in te database
    if the state id exits
    """
    state = storage.get("State", id)

    if state:
        cities = state.cities
        return render_template("9-states.html", states=[state], stateId=id)
    return render_template("9-states.html", states=None, stateId=None)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session after each request"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
