#!/usr/bin/python3
"""
A simple Flask web application that displays:
- "Hello HBNB!" on the root route (/)
- "HBNB" on the /hbnb route
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Displays "Hello HBNB!" when the root route is accessed.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Displays "HBNB" when the /hbnb route is accessed.
    """
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
