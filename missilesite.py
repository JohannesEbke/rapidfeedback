from connection import MissileLauncherConnection, FakeMissileLauncherConnection
from launcher import MissileLauncher
from time import sleep
from argparse import ArgumentParser

import json
import socket

from tornado.web import Application, RequestHandler, StaticFileHandler, HTTPError
from tornado.ioloop import IOLoop, PeriodicCallback

POSITION_X = 0.0
POSITION_Y = 0.0

m = None

class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')

class RocketHandler(RequestHandler):
    def initialize(self, launcher, id):
        self.launcher = launcher
        self.id = id

class PositionHandler(RocketHandler):
    def get(self):
        self.write('X: {} Y: {}\n'.format(*self.launcher.position))

    def post(self, leftright, updown):
        self.launcher.move_to(self.launcher.position[0] + 100*int(leftright), self.launcher.position[1] + 100*int(updown))

class MoveHandler(RocketHandler):
    def get(self, phi, theta):
        print("MoveTo:", phi, theta)
        self.launcher.move_to(float(phi), float(theta))

class FireHandler(RocketHandler):
    def post(self, phi, theta):
        print("Fire at:", phi, theta)
        self.launcher.move_to(float(phi), float(theta), self.launcher.fire)

class CalibrateHandler(RocketHandler):
    def post(self):
        print("Calibrating...")
        self.launcher.calibrate()

def run():
    parser = ArgumentParser()
    parser.add_argument("-f", "--fake", action="store_true", help="Use a fake connection for development")
    parser.add_argument("-i", "--id", default=socket.gethostname(), help="ID of this site")
    args = parser.parse_args()

    if args.fake:
        m = MissileLauncher(FakeMissileLauncherConnection())
    else:
        m = MissileLauncher(MissileLauncherConnection(0))

    config = {
        'launcher': m,
        'id': args.id
    }

    application = Application([
        (r"/position", PositionHandler, config),
        (r"/move/(-?[01])/(-?[01])", PositionHandler, config),
        (r"/move_to/([-0-9.]*)/([-0-9.]*)", MoveHandler, config),
        (r"/fire_at/([-0-9.]*)/([-0-9.]*)", FireHandler, config),
        (r"/calibrate", CalibrateHandler, config),
        (r"/", IndexHandler),
        (r"/static/(.*)", StaticFileHandler, {'path': 'static/'})
    ], debug=True)

    application.listen(7777)
    periodic = PeriodicCallback(m.timestep, 100)
    periodic.start()
    print('Site {} listening at http://{}:7777'.format(args.id, socket.gethostname()))
    IOLoop.instance().start()
