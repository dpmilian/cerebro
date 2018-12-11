#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging.config
import time

import broker.hub as Broker

import settings
from boat import Boat

hub = Broker.Broker()
hub.setPublisher(port=5555)

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def messageLoop(boat):
    # set timer for different frequency of message update; multiples of 100ms (10Hz)
    # don't worry about processing times etc
    ticker = 0              # multiples of 10Hz
    TIMER_10HZ = 0.100        # 100 ms

    while True:
        if ((ticker % 1) == 0):        # 10 Hz
            pass
        if ((ticker % 2) == 0):        # 5 Hz
            loc = boat.vehicle.location.global_frame

            # new PUB/ SUB zmq interface
            the_data = {
                "location": {
                    "lat": loc.lat,
                    "lon": loc.lon,
                    "alt": loc.alt
                },
                "heading": boat.vehicle.heading,
                "attitude": {
                    "roll": boat.vehicle.attitude.roll,
                    "pitch": boat.vehicle.attitude.pitch,
                    "yaw": boat.vehicle.attitude.yaw
                },
                "groundspeed": str(boat.vehicle.groundspeed)
            }
            hub.publish("POS", the_data)

        if ((ticker % 10) == 0):      # 1 Hz
            the_data = {
                "battery": {
                    "voltage": boat.vehicle.battery.voltage,
                    "current": boat.vehicle.battery.current,
                    "level": boat.vehicle.battery.level
                },
                "armed": boat.vehicle.armed,
                "mode": boat.vehicle.mode.name,
                "gps": {
                    "fix_type": boat.vehicle.gps_0.fix_type,
                    "num_sats": boat.vehicle.gps_0.satellites_visible
                }
            }
            hub.publish("STS", the_data)

        ticker += 1
        time.sleep(TIMER_10HZ)


def main():
    connection_string = settings.DEFAULT_SERIAL_PORT
    baud_rate = settings.DEFAULT_BAUD_RATE

    if arg_options.connect:
        connection_string = arg_options.connect
    if arg_options.baud_rate:
        baud_rate = arg_options.baud_rate

    boat = Boat(connection_string, baudrate=baud_rate)
    boat.connect(wait_ready=False)
    vehicle = boat.vehicle

    while not vehicle.attitude.pitch:
        logger.debug(" Waiting for vehicle to initialise...")
        time.sleep(1)

    hub.publish("DBG", "Autopilot: {!s}".format(vehicle.version))
    # logger.debug("Autopilot Firmware version: %s", vehicle.version)
    hub.publish("DBG", "Mode: {}".format(vehicle.mode.name))
    # logger.debug("Mode: %s", vehicle.mode.name)
    # hub.publish("DBG", "System status: {}".format(vehicle.system_status))
    # logger.debug("System status: %s", vehicle.system_status)
    hub.publish("DBG", "Armed: {}".format(vehicle.armed))
    # logger.debug("Armed: %s", vehicle.armed)

    # print (boat.vehicle.groundspeed)

    if arg_options.listen:
        messageLoop(boat)

    if arg_options.goto:
        boat.arm()
        boat.set_mode('GUIDED')
        lat, lon = arg_options.goto.split(',')

        boat.goto(lat, lon)
        boat.vehicle.close()


def get_parser():
    parser = argparse.ArgumentParser(
        description='Command line program to interact with the Pixhawk')
    parser.add_argument(
        "-c", "--connect", help="""Vehicle connection string
        ('/dev/tty.SLAB_USBtoUART', '/dev/cu.usbmodem1', etc.).
        If not specified other parameters, SITL automatically started and used.""")
    parser.add_argument("-b", "--baud-rate", type=int,
                        help="Serial baud rate: 57600 | Usb connection: 115200")
    parser.add_argument("-l", "--listen", action='store_true',
                        help="Listen location, attitude and groundspeed")
    parser.add_argument("-g", "--goto",
                        help="Move to a GPS point (Decimal format). Ex. '42.227870, -8.7218401'")

    return parser


if __name__ == "__main__":

    parser = get_parser()
    arg_options = parser.parse_args()

    main()
