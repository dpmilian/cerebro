import zmq
import sys
import json
import time
import base64
from zmq.eventloop import ioloop, zmqstream

ioloop.install()

def encode(msg):
    return base64.b64encode(msg)

def decode(msg):
    return base64.b64decode(msg)

# ------------------------------
class Broker(object):

    def __init__(self):
        self._publisher = None
        self._suscriber = None
        self._pairs = []

    def __del__(self):
        ioloop.IOLoop.instance().stop()        

    def setPublisher(self, port):
        self._publisher = _Publisher(port)

    def publish(self, topic, message):
        self._publisher.send(topic, message)

    def setSuscriber(self, ip, port):
        self._suscriber = _Suscriber(ip, port)
        self._suscriber.connect()

    def suscribe(self, topics, callback):
        self._suscriber.suscribe(topics, callback)

    # --------
    def listen(self):
        """
        Starts polling the suscribed/ peer sockets already connected to
        Blocks the process/ thread that called it
        """
        ioloop.IOLoop.current(instance=True).start()
    
    def peek(self, topics):
        return self._suscriber.peek(topics)

    def addPeer(self, ip, port):
        pass

# ------------------------------
class _Publisher(object):

    def __init__(self, port):
        self.port = port
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%d" % (self.port))
        print ("ZeroMQ Publisher bound on tcp://*:%d" % (self.port))

    # --------
    def send(self, topic, message):
        json_string = encode(json.dumps(message))
        self.socket.send("%s %s" % (topic, json_string))

# ------------------------------
class _Suscriber(object):

    def __init__(self, ip, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.port = port
        self.ip = ip
        self._stream_sub = None

    # --------
    def connect(self):
            print("Connecting Suscriber to tcp://%s:%d" % (self.ip, self.port))
            errok = self.socket.connect("tcp://%s:%d" % (self.ip, self.port))
            if (errok):
                print("Connection returned error: ")
                print(errok)

    # --------
    def suscribe(self, topics, callback):
        """
        """
        for topic in topics:
            self.socket.setsockopt(zmq.SUBSCRIBE, topic)

        self._stream_sub = zmqstream.ZMQStream(self.socket)
        self._stream_sub.on_recv(callback)



    # --------
    def peek(self, topics):
        """
        Tries to receive message of any of the topics in the array
        does not block; returns the topic and message as a named tuple, or
        if there were no messages, returns topic "BOO"
        """
        for topic in topics:
            self.socket.setsockopt(zmq.SUBSCRIBE, topic)

        try:
            rcvd = self.socket.recv(flags=zmq.NOBLOCK)
            topic, msg = rcvd.split()
            msg = base64.b64decode(msg)

            return (topic, json.loads(msg))

        except zmq.ZMQError:
            topic = 'BOO'
            return ('BOO', None)



