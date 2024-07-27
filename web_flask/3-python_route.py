#!/usr/bin/python3
"""
This script starts a Flask web application with specific routes.
"""

from flask import Flask, request

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!'"""
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display 'HBNB'"""
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Display 'C ' followed by the value of the text variable"""
    return f"C {text.replace('_', ' ')}"

@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """Display 'Python ' followed by the value of the text variable"""
    return f"Python {text.replace('_', ' ')}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

