#!/usr/bin/env python3
"""Flask app with Babel"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext as _

app = Flask(__name__, template_folder='templates')
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Config class for Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale() -> str:
    """Get best matching locale from request"""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    user = getattr(g, 'user', None)
    if user:
        return user.get('locale')
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> dict:
    """Get user from request"""
    user_id = request.args.get('login_as')
    if user_id and int(user_id) in users:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """Set user before request"""
    g.user = get_user()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """Index route"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
