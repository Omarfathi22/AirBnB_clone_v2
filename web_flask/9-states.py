#!/usr/bin/python3
"""Starts a Flask web application to display states and cities"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()

@app.route('/states', strict_slashes=False)
def states_list():
    """Displays a list of all states"""
    states = storage.all(State).values()
    return render_template('9-states.html', states=states)

@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Displays cities of a specific state"""
    states = storage.all(State).values()
    state = None
    for s in states:
        if s.id == id:
            state = s
            break
    return render_template('9-states.html', state=state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

