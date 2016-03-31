import flask
import flask_sqlalchemy
import os

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

HOST = "127.0.0.1"
PORT = 3000
DEBUG = True

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///classcloud.sqlite"
db = flask_sqlalchemy.SQLAlchemy(app)

##########
# Models #
##########

class File(db.Model):
  id = db.Column(db.String(), primary_key=True)
  path = db.Column(db.String(), unique=True)

  def __init__(self, id, path):
    self.id = id = username
    self.path = path

##########
# Routes #
##########

# Route to test connections to this server.
@app.route("/test")
def test():
  return "Success.", 200

#######
# Run #
#######

if __name__ == "__main__":
	db.drop_all()
	db.create_all()
	app.run(host=HOST, port=PORT)
