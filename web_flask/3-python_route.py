#!/usr/bin/python3
"""
A simple Flask web application that displays:
- "Hello HBNB!" on the root route (/)
- "HBNB" on the /hbnb route
- "C <text>" on the /c/<text> route, replacing underscores with spaces.
- "Python <text>" on the /python/<text> route, replacing underscores
with spaces. The default value of `text` is "is cool".
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


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Displays "C <text>", replacing underscores with spaces.
    """
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python/', strict_slashes=False)
def python_text(text="is cool"):
    """
    Displays "Python <text>", replacing underscores with spaces.
    The default value of `text` is "is cool".
    """
    return "Python {}".format(text.replace('_', ' '))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
