# Fanequinha Autonomous Boat Project

from datamgr import DataManager


def test_connection():
    datamgr = DataManager()
    assert datamgr is not None

    datamgr.initialize()
