#!/usr/bin/env python
from flask.ext.script import Manager, Server

from devilsdictionary.app import app

manager = Manager(app)

@manager.command
def runserver():
  app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
  manager.run()
