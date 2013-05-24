import os
from flask import Flask
from flask.ext.restful import Resource,  reqparse, Api
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

app = Flask("flasktestexample")
api = Api(app)
app.debug = True

if os.environ.get('DATABASE_URL') is None:
  engine = create_engine('postgres://flaskexample:flask@localhost:5432/flaskexample', convert_unicode=True)
else:
  engine = create_engine(os.environ['DATABASE_URL'], convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

@app.teardown_request
def teardown_request(exception):
    db_session.remove()


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

#User Model
class User(Base):
    __tablename__ = 'users'

    #from http://stackoverflow.com/a/11884806
    def as_dict(self):
      return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = Column(Integer, primary_key=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    email = Column(String(200), unique=True)

#Parser arguments that Flask-Restful will check for
parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, required=True, help="First Name Cannot Be Blank")
parser.add_argument('last_name', type=str, required=True, help="Last Name Cannot Be Blank")
parser.add_argument('email', type=str, required=True, help="Email Cannot Be Blank")

#Flask Restful Views
class UserView(Resource):
  def get(self, id):
    e = User.query.filter(User.id == id).first()
    if e is not None:
      return e.as_dict()
    else:
      return {}


class UserViewList(Resource):
  def get(self):
    results = []
    for row in User.query.all():
      results.append(row.as_dict())
    return results

  def post(self):
      args = parser.parse_args()
      o = User()
      o.first_name = args["first_name"]
      o.last_name = args["last_name"]
      o.email = args["email"]

      try:
        db_session.add(o)
        db_session.commit()
      except IntegrityError, exc:
        return {"error": exc.message}, 500

      return o.as_dict(), 201

#Flask Restful Routes
api.add_resource(UserViewList, '/users')
api.add_resource(UserView, '/users/<string:id>')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
