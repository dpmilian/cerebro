# Fanequinha Autonomous Boat Project

import datetime
import json
import logging.config

import zmq
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import model
from model import VehicleEvent

# Module logger
logger = logging.getLogger(__name__)


class DataManager():
    """
    The DataManager currently handles event data storage. It currently listens to every event
    and stores them to a SQLite database.

    TODO: Spool event writes, store in a single transaction every N events and or N seconds
    TODO: Later on, each component could handle and maybe decimate some events (POS rate is high)
    """

    def __init__(self, db_url="sqlite:///fanequinha.sqlite3"):
        """
        """
        self.db_url = db_url

    def initialize(self):
        """
        Initializes the component: connects to ZMQ, database...
        """
        # Create SQLAlchemy database engine
        self.db_engine = create_engine(self.db_url)  # echo=True

        # Enable SQLite WAL mode (write ahead log). Reduces disk IO and improves DB concurrency.
        db_connection = self.db_engine.connect()
        db_connection.execute("PRAGMA journal_mode=WAL")
        db_connection.close()

        # Use SQLAlchemy metadata method to create database schema
        model.Base.metadata.create_all(self.db_engine)

        Session = sessionmaker(bind=self.db_engine)
        self.db_session = Session()

    def start(self):
        # Create a thread for the listener loop
        # self.listener_thread = threading.Thread(target=self.listener_loop)
        # self.listener_thread.daemon = True
        # self.listener_thread.start()

        self.listener_loop()

    def listener_loop(self):
        """
        Listens for published events and write them to database.

        TODO: Unify with broker client module.
        """
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        # We can connect to several endpoints if needed, and receive from all.
        socket.connect('tcp://127.0.0.1:5555')

        # Declare the socket as of type SUBSCRIBER and provide a prefix filter.
        # For now, the filter is the empty string (all topics).
        socket.setsockopt(zmq.SUBSCRIBE, b'')

        # Process incoming messages
        while True:
            message = socket.recv()
            msg_dt = datetime.datetime.utcnow()
            try:
                msg_parts = message.split(b' ', 1)
                msg_topic = msg_parts[0].decode()
                msg_data = json.loads(msg_parts[1].decode())
                logger.debug("Received message (topic=%s): %s", msg_topic, msg_data)

            except Exception as e:
                logger.error("Error decoding received message: %r (%s)", message, e)

            # Process event
            self.process_message(msg_dt, msg_topic, msg_data)

    def process_message(self, dt, topic, data):
        """
        """
        self.store_message(dt, topic, data)

    def store_message(self, dt, topic, data):
        """
        """
        # logger.debug("Storing event in database (topic=%s, data=%s): %s", topic, data)
        event = VehicleEvent(dt=dt,
                             type=topic,
                             data=json.dumps(data))
        try:
            self.db_session.add(event)
            self.db_session.commit()
        except Exception as e:
            logger.error("Could not store event in database (topic=%s, data=%s): %s", topic, data, e)
            self.db_session.rollback()
