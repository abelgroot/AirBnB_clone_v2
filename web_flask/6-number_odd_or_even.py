#!/usr/bin/python3
"""
A simple Flask web application that displays:
- "Hello HBNB!" on the root route (/)
- "HBNB" on the /hbnb route
- "C <text>" on the /c/<text> route, replacing underscores with spaces.
- "Python <text>" on the /python/<text> route, replacing underscores with
  spaces. The default value of `text` is "is cool".
- "<n> is a number" on the /number/<n> route, only if `n` is an integer.
- An HTML page with "Number: n" on the /number_template/<n> route, only
  if `n` is an integer.
- An HTML page with "Number: n is even|odd" on the /number_odd_or_even/<n>
  route, only if `n` is an integer.
"""

from flask import Flask, render_template

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


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """
    Displays "<n> is a number" only if `n` is an integer.
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Displays an HTML page with "Number: n" only if `n` is an integer.
    """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """
    Displays an HTML page with "Number: n is even|odd"
    only if `n` is an integer.
    """
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
