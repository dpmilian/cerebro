import time

from boat import Boat


def test_connection(connection_parameters):
    boat = Boat(**connection_parameters)
    boat.connect(wait_ready=False)

    assert boat.vehicle is not None

    boat.vehicle.close()


def test_wait_armable_vehicle(connection_parameters):
    boat = Boat(**connection_parameters)
    boat.connect(wait_ready=False)

    while not boat.vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    assert boat.vehicle.is_armable

    boat.vehicle.close()


def test_vehicle_mode(connection_parameters):
    boat = Boat(**connection_parameters)
    boat.connect(wait_ready=False)

    boat.set_mode('GUIDED')

    assert boat.vehicle.mode.name == 'GUIDED'

    boat.vehicle.close()


def test_vehicle_armed(connection_parameters):
    boat = Boat(**connection_parameters)
    boat.connect(wait_ready=False)

    boat.arm()

    assert boat.vehicle.armed

    boat.vehicle.close()


def test_set_sail(connection_parameters):
    boat = Boat(**connection_parameters)

    boat.connect()
    boat.arm()
    boat.set_mode('GUIDED')

    lat_point = 42.227870
    long_point = -8.719468

    boat.goto(latitude=lat_point, longitude=long_point, ground_speed=10)

    while boat.vehicle.location.global_frame.lat < lat_point:
        time.sleep(1)

    assert 42.227860 < boat.vehicle.location.global_frame.lat < 42.227890

    boat.vehicle.close()
