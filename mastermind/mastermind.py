import broker.hub as Broker
import json                             # only to visualize the json objects for debugging
from multiprocessing import Process

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

# ------------------------------
def main():
    hub = Broker.Broker()
    hub.setSuscriber("localhost", 5555)
    hub.suscribe(["POS", "STS", "DBG"], process_message)     # Probably should run in a process
    hub.listen()    
    while(True):
        # Doing other mastermind stuff that is really cool
        print ("#")
        sleep(500)

if __name__ == "__main__":

    main()