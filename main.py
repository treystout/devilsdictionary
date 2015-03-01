#!/usr/bin/env python
import json
import logging
import os
import requests
import sys

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
        #"Content-Type": "application/json",
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
    resp = self._hit('POST', 'oauth/token', auth=auth, data=params)
    payload = resp.json()
    log.debug("token response: %s", payload)
    self.__token = payload.get('access_token')

  def get_handwritings(self):
    r = self._hit("GET", "v1/handwritings")
    log.debug("repsonse for handwritings %s", r)


if __name__ == "__main__":
    api = GEAPI("https://api-staging.graciouseloise.com/",
        "2404cdc31a69a95f635bbe36d87b41342ce20a89cd13b4911b0df2a9982a1323",
        "38d7f351a1b902368356e90d648d3f02645b859d8caa9f8d9872f8750fa279bd")
    handwritings = api.get_handwritings()

