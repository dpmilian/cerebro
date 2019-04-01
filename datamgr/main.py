#!/usr/bin/env python

# Fanequinha Autonomous Boat Project

import argparse
import logging

from datamgr import DataManager

# Module logger
logger = logging.getLogger(__name__)


def initialize_logging(debug=False):
    # In absence of file config
    default_level = logging.INFO if not debug else logging.DEBUG
    logging.basicConfig(format='%(asctime)s - %(module)s - %(levelname)s - %(message)s', level=default_level)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Data logger: stores events to database.')
    parser.add_argument("-d", "--debug", action='store_true', dest="debug", help="Debug mode.")

    options = parser.parse_args()
    return options


def main(options):
    logger.debug("Logging DEBUG level is enabled.")
    logger.info("Starting application.")

    datamgr = DataManager()
    datamgr.initialize()
    datamgr.start()


if __name__ == "__main__":

    options = parse_arguments()
    initialize_logging(debug=options.debug)

    main(options)
