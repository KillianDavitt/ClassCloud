#!/usr/bin/python3
import flask
import flask_sqlalchemy
import os
from werkzeug import secure_filename
import random
import string

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

HOST = "127.0.0.1"
PORT = 3000
DEBUG = True
TOKEN_PATH = os.path.join(DIRECTORY, "classcloud.token")
UPLOAD_FOLDER = "files"
FILE_ID_LENGTH = 10

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///classcloud.sqlite"
db = flask_sqlalchemy.SQLAlchemy(app)
token = None

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
  filename = db.Column(db.String(20), unique=False)

  def __init__(self, id, path, filename):
    self.id = id
    self.path = path
    self.filename = filename

##########
# Routes #
##########

# list all files.
@app.route("/list_files", methods=["GET"])
def list_files():
  print("start")
  data = flask.request.get_json()
  print("data")
  if not data or data["token"] != token:
    return "Invalid Token", 400
  return json.dumps(file.path for file in File.query.all()), 200

@app.route("/put_file", methods=["POST"])
def put_file():
  data = request.get_json()
  if not data or data["token"] != USER_TOKEN:
  	return "Invalid Token", 400
  file = request.files["file"]
  if file:
    filename = secure_filename(file.filename)
    files = File.query.filter_by(path=data['path'], filename=filename).first()

    if not files:
      return "A file in this directory already exists", 400

    # Gen id, A-Z, a-z, 0-9


    new_file = File(id=gen_id(), path=data['path'], filename=filename)

    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return "Ok", 200

def gen_id():
  return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(FILE_ID_LENGTH))


def put_file():
	pass

#######
# Run #
#######

if __name__ == "__main__":
  db.drop_all()
  db.create_all()
  token = get_token()
  if token:
  	app.run(host=HOST, port=PORT)
  else:
  	print("Could not read token.\nExiting...")


