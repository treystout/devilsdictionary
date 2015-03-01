import base64
import logging
import requests

from flask import Blueprint, render_template as T, session, redirect, url_for, \
    request as R, flash, g, jsonify, abort, current_app

log = logging.getLogger(__name__)
mod = Blueprint('general', __name__)

from devilsdictionary.words import word_dict, word_list
from devilsdictionary.GEAPI import GEAPI

gracious_api = GEAPI(
  "https://api-staging.graciouseloise.com/",
  "2404cdc31a69a95f635bbe36d87b41342ce20a89cd13b4911b0df2a9982a1323",
  "38d7f351a1b902368356e90d648d3f02645b859d8caa9f8d9872f8750fa279bd")

@mod.route('/')
def index():
  return T("index.j2", words=word_list)

@mod.route('/define/<word>/')
def definition(word):
  w = word_dict.get(word)
  if not w:
    abort(404)

  handwritings = gracious_api.get_handwritings()

  return T("definition.j2", word=word, part=w['part'],
      definition=w['definition'], handwritings=handwritings)

@mod.route('/render/<word>/<hw_id>/')
def render(word, hw_id):
  w = word_dict.get(word)
  if not w:
    abort(404)

  to_write = """%s (%s)
  %s
  """ % (word, w['part'], w['definition'])
  log.debug("will render %s in HW %s", word, hw_id)

  img = gracious_api.render(hw_id, to_write, 5, 3)
  url = img['_links']['screen_file']['href']
  log.debug("image created at %s", url)

  import time
  time.sleep(8)

  r = requests.get(url, headers={'Authorization': 'Bearer %s' % \
      gracious_api.HACK_token()}, stream=True)

  if r.status_code == 200:
    r.raw.decode_content = True
    rendered = base64.b64encode(r.raw.read())

  return T("definition.j2", word=word, part=w['part'],
      definition=w['definition'], rendered=rendered)
