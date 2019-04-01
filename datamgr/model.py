# Fanequinha Autonomous Boat Project

import logging.config

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime

# Module logger
logger = logging.getLogger(__name__)


Base = declarative_base()


class VehicleEvent(Base):
    """
    """

    __tablename__ = 'vehicleevent'

    id = Column(Integer, primary_key=True)

    dt = Column(DateTime)

    type = Column(String)

    data = Column(String)  # Stores JSON data

    def __repr__(self):
        return "<VehicleEvent(dt=%s, type='%s', data=%s)>" % (
            self.dt, self.type, self.data)
