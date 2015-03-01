import logging
import os.path

from flask import Blueprint, render_template as T, session, redirect, url_for, \
    request as R, flash, g, jsonify, abort, current_app

log = logging.getLogger(__name__)
mod = Blueprint('general', __name__)

@mod.route('/')
def index():
  return T("index.j2")
