"""\
An entity in a swarm.
"""

import zmq

from threading import Thread, Event
from universe import Universe

class Entity(object):
    launcher = Thread

    def __init__(self):
        self.ctx = zmq.Context.instance(2)
        self.ioloop = self.launcher(target=self.run)
        self.shutdown = Event

    def start(self):
        self.ioloop.start()

    def join(self):
        self.shutdown.set()
        self.ioloop.join()

    def run(self):
        medium = self.ctx.socket(zmq.SUB)
        medium.connect(Universe.medium_endpoint)
        broadcast = self.ctx.socket(zmq.PUSH)
        broadcast.connect(Universe.broadcast_endpoint)

        poller = zmq.Poller()
        poller.register(medium, zmq.POLLIN)

        while not self.shutdown.is_set():
            socks = dict(poller.poll(100))

            if medium in socks:
                msg = medium.recv_multipart()
                print(msg)

