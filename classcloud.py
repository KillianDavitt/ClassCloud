#!/usr/bin/python3
import flask
import flask_sqlalchemy
import os
from werkzeug import secure_filename

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

HOST = "127.0.0.1"
PORT = 3000
DEBUG = True
TOKEN_PATH = os.path.join(DIRECTORY, "classcloud.token")

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///classcloud.sqlite"
db = flask_sqlalchemy.SQLAlchemy(app)

# return token or None
def get_token():
	try:
		with open(TOKEN_PATH) as f:
			return f.read().strip()
	except Exception as e:
		print("Couldn't read token: %r" % e)
		return None

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
@app.route("/list_files")
def list_files():
  return "Success.", 200

@app.route("/get_file", methods=["POST"])
def get_file():
  data = request.get_json()
  if data["token"] == USER_TOKEN:
    file = request.files["file"]
    if file:
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return "Ok", 200
    else:
      return "Invalid Token", 400

def put_file():
	pass

#######
# Run #
#######

if __name__ == "__main__":
  db.drop_all()
  db.create_all()
  app.run(host=HOST, port=PORT)
