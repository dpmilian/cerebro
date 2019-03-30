![Logo](https://farmalandiablog.es/wp-content/uploads/2017/07/faneca-brava-rei-zentolo.jpg)
# Broker

Work in progress!!!

## Requirements

- Python 2.7

# Description 

All functionality is in the broker package, module hub
The Broker is configured as a zmq PUB/ SUB, any client should be able
to connect to any other node. 

A node that wants to publish would include a Publisher object; a node that wants to suscribe to a topic would include a Suscriber object

In this basic proof of concept, main.py from commander creates a Publisher node, and sends information on a topic "TLM":

```
pub = Broker.Publisher(port=5555)

// ...

listen_data = {
            "location": str(boat.location),
            "attitude": str(boat.vehicle.attitude),
            "groundspeed": str(boat.vehicle.groundspeed)
        }
        pub.send("TLM", listen_data)
```

To test the suscriber, inside broker/ run hub.py, this creates a 
suscriber connection to port 5555 on localhost, and listens to 
messages from the topic "TLM" (and zmq filters out the rest of topics)

```
bksrv = Suscriber("localhost", 5555)
    bksrv.connect()
    bksrv.listen("TLM")
```
