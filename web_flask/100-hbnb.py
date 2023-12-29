#!/usr/bin/python3

"""
A script that starts a Flask web application

The web application listens on 0.0.0.0, port 5000

Routes:
        /hbnb: display a HTML page with main hbnb site
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display a complete HTML page with filters"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    return render_template("100-hbnb.html", 
                           states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session after each request"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
