#!/usr/bin/env python
import json
import logging
import os
import requests
import shutil
import sys
import uuid

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger('GEAPI')


class GEAPI(object):
  def __init__(self, url_base, app_token, app_secret, timeout_sec=30):
    self.url_base = url_base
    self.app_token = app_token
    self.app_secret = app_secret
    self.timeout_sec = timeout_sec
    self.__token = None # this is set via get_token()
    self.get_token()

  def _hit(self, method, url, extra_headers=None, **kwargs):
    """Perform an HTTP operation where method is the HTTP method (GET,
    POST etc...), and url is relative to the URLBASE
    """
    full_url = "%s%s" % (self.url_base, url)
    log.debug("sending %s for %s", method, full_url)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if self.__token:
      headers["Authorization"] = "Bearer %s" % self.__token
    if extra_headers:
      headers.update(extra_headers)
    log.debug("REQUEST HEADERS: %s", headers)

    try:
      resp = requests.request(method, full_url, headers=headers,
          timeout=self.timeout_sec, **kwargs)
    except requests.exceptions.RequestException as e:
        log.exception("Failed API call to %s: %s", url, e)
        raise
    log.debug(resp.text)
    log.debug(resp.status_code)
    log.debug("RESPONSE HEADERS: %s", resp.headers)
    return resp

  def get_token(self):
    log.debug("getting token")
    auth = (self.app_token, self.app_secret)
    params = {
       "grant_type": "client_credentials",
       "scope": "handwriting image package package:list application_full_mode",
    }
    resp = self._hit('POST', 'oauth/token', auth=auth, json=params)
    payload = resp.json()
    log.debug("token response: %s", payload)
    self.__token = payload.get('access_token')

  def HACK_token(self):
    """This is only here to get around downloading images for test
    """
    return self.__token

  def get_handwritings(self):
    r = self._hit("GET", "v1/handwritings")
    return r.json().get('handwritings', [])

  def render(self, hw_id, text, width_inches, height_inches):
    payload = {
        'name': str(uuid.uuid4()),
        'data': {
          'text': text,
          'handwriting_id': hw_id,
          'width': '%sin' % width_inches,
          'height': '%sin' % height_inches,
        }
      }
    r = self._hit("POST", "v1/images", json=payload)
    return r.json().get('image')


if __name__ == "__main__":
    api = GEAPI("https://api-staging.graciouseloise.com/",
        "2404cdc31a69a95f635bbe36d87b41342ce20a89cd13b4911b0df2a9982a1323",
        "38d7f351a1b902368356e90d648d3f02645b859d8caa9f8d9872f8750fa279bd")
    handwritings = api.get_handwritings()
    for h in handwritings:
      print h.get('id'), h.get('name')

    img = api.render(handwritings[0]['id'],
        "this is some sample text!", 5, 3)
    url = img['_links']['screen_file']['href']
    print "getting", url

    import time
    time.sleep(10)

    r = requests.get(url, headers={'Authorization': 'Bearer %s' % api.HACK_token()},
        stream=True)
    if r.status_code == 200:
      with open("out.png", "wb") as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

