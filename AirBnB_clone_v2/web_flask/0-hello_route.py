#!/usr/bin/python3
"""
Flask web application script that listens on 0.0.0.0:5000 and
responds with 'Hello HBNB!' at the root route.
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """returns Hello HBNB!"""
    return 'Hello HBNB!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
