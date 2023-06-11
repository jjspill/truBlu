"""trublu package initializer."""
import flask

app = flask.Flask(__name__)

app.config.from_object('trublu.config')

app.config.from_envvar('trublu_SETTINGS', silent=True)

import trublu.views  # noqa: E402  pylint: disable=wrong-import-position
import trublu.model  # noqa: E402  pylint: disable=wrong-import-position
