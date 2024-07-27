#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """Displays an HTML page with a list of all State objects in DBStorage and their Cities.

    States and cities are sorted by name.
    """
    # Retrieve all states and cities from storage
    states = storage.all("State")
    # For each state, retrieve the list of cities
    for state in states.values():
        if hasattr(state, 'cities'):
            cities = sorted(state.cities, key=lambda city: city.name)
        else:
            # Handle the case where cities might not be a direct attribute
            cities = sorted(storage.all("City").values(), key=lambda city: city.name)
        state.cities = cities

    # Sort states by name
    sorted_states = sorted(states.values(), key=lambda state: state.name)
    
    return render_template("8-cities_by_states.html", states=sorted_states)

@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

