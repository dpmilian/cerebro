from __future__ import print_function

import logging
import time

import dronekit

import utils

logger = logging.getLogger(__name__)


class Boat(object):

    def __init__(self, connection_string, baudrate=None):
        self.connection_string = connection_string
        self.baudrate = baudrate
        self._vehicle = None

    def connect(self, wait_ready=True):
        self._vehicle = dronekit.connect(self.connection_string,
                                         baud=self.baudrate,
                                         wait_ready=wait_ready)

    def set_mode(self, mode):
        self._vehicle.mode = dronekit.VehicleMode(mode)

        while not self._vehicle.mode.name == mode:
            logger.debug('Waiting for mode change to %s...', mode)
            time.sleep(1)

    def arm(self):
        self._vehicle.armed = True
        while not self._vehicle.armed:
            logger.debug('Waiting for arming...')
            time.sleep(1)

    def disarm(self):
        self._vehicle.armed = False
        while self._vehicle.armed:
            logger.debug('Waiting for disarming...')
            time.sleep(1)

    @property
    def vehicle(self):
        return self._vehicle

    def goto(self, latitude, longitude, ground_speed=None):
        destination = dronekit.LocationGlobalRelative(float(latitude),
                                                      float(longitude), 0)
        self._vehicle.simple_goto(destination, groundspeed=ground_speed)

        while self._vehicle.groundspeed < 3:
            time.sleep(1)
            logger.debug('Speed up groundspeed...%s', self._vehicle.groundspeed)
        return

    def moveto(self, x, y):
        destination = utils.get_location_metres(
            self.vehicle.location.global_relative_frame, x, y)
        self._vehicle.simple_goto(destination, groundspeed=None)
        return destination

    @property
    def location(self):
        lat = self._vehicle.location.global_relative_frame.lat
        lon = self._vehicle.location.global_relative_frame.lon

        return lat, lon
