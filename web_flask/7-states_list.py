#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/states_list", strict_slashes=False)
def states_list():
    """Displays an HTML page with a list of all State objects in DBStorage.

    States are sorted by name.
    """
    # Retrieve all states from storage and sort by name
    states = storage.all("State")
    # Convert the dictionary values to a list and sort by the 'name' attribute
    sorted_states = sorted(states.values(), key=lambda state: state.name)
    return render_template("7-states_list.html", states=sorted_states)

@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

