import os
import base64
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

from application import init_db, db_session

init_db()

import application
test_app = application.app.test_client()

def teardown():
  db_session.remove()