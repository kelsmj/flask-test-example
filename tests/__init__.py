from application import init_db, db_session

init_db()

import application
test_app = application.app.test_client()

def teardown():
  db_session.remove()