from connection import MissileLauncherConnection, FakeMissileLauncherConnection
from launcher import MissileLauncher
from time import sleep
from argparse import ArgumentParser
import json

from tornado.web import Application, RequestHandler, StaticFileHandler, HTTPError
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.httpclient import HTTPClient


class TargetHandler(RequestHandler):
    def initialize(self, targets):
        self.targets = targets
        self.http_client = HTTPClient()

    def post(self, target):
        url, (x, y) = self.targets[target]
        print("Firing on {} at {} (coords {}/{})".format(target, url, x, y))
        self.http_client.fetch("{}/fire_at/{}/{}".format(url, x, y), method="POST", body="A Rocket")

def run():
    parser = ArgumentParser()
    parser.add_argument("-t", "--targets", help="File with 'targetid x y' tuples in range of this rocket launcher")
    parser.add_argument("-s", "--sites", help="File with site_id and URL")
    args = parser.parse_args()

    sites = {}
    if args.sites:
        for site_line in open(args.sites).readlines():
            site_id, url = site_line.split()
            sites[site_id] = url

    targets = {}
    if args.targets:
        for person_line in open(args.targets).readlines():
            name, site, x, y = person_line.split()
            targets[name] = sites[site], map(float, (x, y))

    config = {
        'targets': targets
    }

    application = Application([
        (r"/fire_at/([^/]*)", TargetHandler, config)
    ], debug=True)

    application.listen(6666)
    print('Listening at http://localhost:6666')
    IOLoop.instance().start()
