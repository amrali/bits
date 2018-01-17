"""\
A universe shared by every swarm member to communicate and announce needs.
"""

import zmq

from threading import Thread, Event

class Universe(object):
    medium_endpoint = "ipc:///tmp/universe.medium"
    broadcast_endpoint = "ipc:///tmp/universe.broadcast"
    launcher = Thread

    def __init__(self):
        self.ctx = zmq.Context.instance(2)
        self.ioloop = self.launcher(target=self.run)
        self.shutdown = Event()

    def start(self):
        self.ioloop.start()

    def join(self):
        self.shutdown.set()
        self.ioloop.join()

    def run(self):
        medium = self.ctx.socket(zmq.PUB)
        medium.bind(medium_endpoint)
        broadcast = self.ctx.socket(zmq.PULL)
        broadcast.bind(broadcast_endpoint)

        poller = zmq.Poller()
        poller.register(broadcast, zmq.POLLIN)

        while not self.shutdown.is_set():
            socks = dict(poller.poll(100))

            if broadcast in socks:
                msg = broadcast.recv_multipart()
                print(msg)
                medium.send_multipart(msg)

