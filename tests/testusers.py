import json
from nose.tools import *

from tests import test_app

def check_content_type(headers):
  eq_(headers['Content-Type'], 'application/json')

def test_user_routes():
  rv = test_app.get('/users')
  check_content_type(rv.headers)
  resp = json.loads(rv.data)
  #make sure we get a response
  eq_(rv.status_code,200)
  #make sure there are no users
  eq_(len(resp), 0)

  #create a user
  d = dict(first_name="User1First", last_name="User1Last",email="User1@User1.com")
  rv = test_app.post('/users', data=d)
  check_content_type(rv.headers)
  eq_(rv.status_code,201)

  #Verify we sent the right data back
  resp = json.loads(rv.data)
  eq_(resp["email"],"User1@User1.com")
  eq_(resp["first_name"],"User1First")
  eq_(resp["last_name"],"User1Last")

  #Get users again...should have one
  rv = test_app.get('/users')
  check_content_type(rv.headers)
  resp = json.loads(rv.data)
  #make sure we get a response
  eq_(rv.status_code,200)
  eq_(len(resp), 1)

  #GET the user with specified ID
  rv = test_app.get('/users/%s' % resp[0]['id'])
  check_content_type(rv.headers)
  eq_(rv.status_code,200)
  resp = json.loads(rv.data)
  eq_(resp["email"],"User1@User1.com")
  eq_(resp["first_name"],"User1First")
  eq_(resp["last_name"],"User1Last")

  #Try and add Duplicate User Email
  rv = test_app.post('/users', data=d)
  check_content_type(rv.headers)
  eq_(rv.status_code,500)