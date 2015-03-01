import logging
import urllib

from flask import Flask

from . import config

log = logging.getLogger(__name__)

# create the main app
app = Flask(__name__, static_url_path="")
app.config.from_object(config)
app.debug= config.DEBUG

from .views import general
app.register_blueprint(general.mod)
