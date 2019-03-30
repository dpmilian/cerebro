import os

USE_SITL = os.environ.get('USE_SITL', True)
# Add your custom serial port
# (http://python.dronekit.io/guide/connecting_vehicle.html#get-started-connecting)
DEFAULT_SERIAL_PORT = os.environ.get('SERIAL_PORT', '/dev/cu.usbmodem1')
# Add port baud rate. Tipically 57600 for serial, 115200 for USB.
# Check PixHawk TELEM 1 configuration in case connection problems.
DEFAULT_BAUD_RATE = os.environ.get('BAUD_RATE', 115200)


LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': (
                '%(asctime)s'
                ' pid=%(process)d'
                ' level=%(levelname)s'
                ' logger=%(name)s'
                ' %(message)s'
            )
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'commander.log',
            'formatter': 'verbose',
            'level': 'DEBUG',
        }
    },
    'loggers': {
        'commander': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_handler'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file_handler'],
    },
}
