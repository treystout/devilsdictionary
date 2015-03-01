import logging

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
  return T("definition.j2", word=word, part=w['part'],
      definition=w['definition'])

@mod.route('/render/<word>/')
def render(word):
  w = word_dict.get(word)
  if not w:
    abort(404)

  to_write = """%s (%s)
  %s
  """ % (word, w['part'], w['definition'])

  gracious_api.render(to_write)
  return T("definition.j2", word=word, part=w['part'],
      definition=w['definition'])
