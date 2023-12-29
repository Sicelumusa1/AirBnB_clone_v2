#!/usr/bin/python3

"""
A script that starts a Flask web application

The web application listens on 0.0.0.0, port 5000

Routes:
        /states_list: display a HTML page with list of 
                      states in te database
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display a HTML page with list of states in te database"""
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session after each request"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
