import pytest
from dronekit_sitl import SITL

import settings


def start_sitl_rover():
    '''start a SITL session using sensible defaults.
    This should be the simplest way to start a sitl session'''
    print("Starting copter simulator (SITL)")
    sitl = SITL()
    sitl.download('rover', '2.50', verbose=True)

    sitl_args = ['-I0', '--model', 'rover', '--home=42.2278287,-8.72184010,584,353']
    sitl.launch(sitl_args, await_ready=False, restart=True, verbose=True)
    sitl.block_until_ready(verbose=True)
    return sitl


@pytest.fixture
def connection_parameters():
    connection_string = settings.DEFAULT_SERIAL_PORT
    baud_rate = settings.DEFAULT_BAUD_RATE

    if settings.USE_SITL is True:
        sitl = start_sitl_rover()
        connection_string = sitl.connection_string()

    return {'connection_string': connection_string, 'baudrate': baud_rate}
