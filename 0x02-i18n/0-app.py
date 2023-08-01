#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, render_template
app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """Index route"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
