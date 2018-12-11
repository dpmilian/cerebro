import broker.hub as Broker
import json                             # only to visualize the json objects for debugging
from multiprocessing import Process
from time import sleep

# ------------------------------
class Mastermind(object):
    def __init__(self):
        self.hub = Broker.Broker()
        self.guided = None
        self.obstacle_detected = False
        self.waypoints = []
        # other state info...

    def events(self):
        self.hub.setSuscriber("localhost", 5555)
        self.hub.suscribe(["POS", "STS", "DBG"], process_message)     # Probably should run in a process
        # thread.start_new_thread(self.hub.listen,())
        self.hub.listen()

    def run(self):
        while(True):
            # Doing other mastermind stuff that is really cool
            print ("#")
            sleep(.05)

# ------------------------------
def process_message(rcvd):
    
    topic, msg = rcvd[0].split()
    msg = Broker.decode(msg)

    if (topic == 'DBG'):
        print("[%s]: %s" % (topic, msg))
    else:
        print("[%s] Received message:" % (topic))
        print (json.dumps(msg, indent=4, sort_keys=True))
    #     print ("[%s] Received message: %s" % (topic, msg))


mastermind = Mastermind()
Process(mastermind.events())
# mastermind.run()
