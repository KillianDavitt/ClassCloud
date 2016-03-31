#!/usr/bin/python3
import flask
import flask_sqlalchemy
import json
import os
import random
import shutil
import string
import werkzeug

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

HOST = "127.0.0.1"
PORT = 3000
DEBUG = True
TOKEN_PATH = os.path.join(DIRECTORY, "classcloud.token")
UPLOAD_FOLDER = os.path.join(DIRECTORY, "files")
FILE_ID_LENGTH = 10

# return token or None
def get_token():
  try:
    with open(TOKEN_PATH) as f:
      return f.read().strip()
  except Exception as e:
    print("Couldn't read token: %r" % e)
    return None

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///classcloud.sqlite"
db = flask_sqlalchemy.SQLAlchemy(app)
token = get_token()

def empty_folder(folder):
  for file in os.listdir(folder):
    file_path = os.path.join(folder, file)
    try:
      if os.path.isfile(file_path):
        os.unlink(file_path)
      elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
    except Exception as e:
      print("Could not delete file %s: %r" % (file_path, e))

##########
# Models #
##########

class File(db.Model):
  id = db.Column(db.String(), primary_key=True)
  path = db.Column(db.String())
  filename = db.Column(db.String(20))

  def __init__(self, id, path, filename):
    self.id = id
    self.path = path
    self.filename = filename

  def full_path(self):
    return os.path.join(UPLOAD_FOLDER, os.path.join(self.path, self.filename))

##########
# Routes #
##########

# list all files.
@app.route("/list_files", methods=["GET"])
def list_files():
  data = flask.request.get_json()
  if not data:
    return "No token", 400
  if data.get("token", None) != token:
    return "Invalid token", 400
  files = [[file.id, file.full_path()] for file in File.query.all()]
  files.sort(key=lambda x: x[1]) # sort by full path
  return flask.jsonify(files=files), 200

# add a file
@app.route("/put_file", methods=["POST"])
def put_file():
  data = flask.request.get_json()
  # json
  if not data:
    return "No json", 400
  # token
  if data.get("token", None) != token:
    return "Invalid token", 400
  # path
  path = data.get("path", None)
  if not path:
    return "No path", 400
  # filename
  filename = data.get("filename", None)
  if not filename:
    return "No filename", 400
  filename = werkzeug.secure_filename(filename)
  # file data
  file_data = data.get("file", None)
  if not file_data:
    return "No file", 400
  # check if already exists
  f = File.query.filter_by(path=path, filename=filename).first()
  if f:
    print(f.filename)
    return "File already exists", 400
  # new File object
  file = File(gen_id(), path, filename)
  # create directories in path and create file
  try:
    os.makedirs(os.path.dirname(file.full_path()), exist_ok=True)
    with open(file.full_path(), "w") as f:
      f.write(str(file_data))
  except Exception as e:
    return "Could not create file.", 400
  # save File to database
  db.session.add(file)
  db.session.commit()
  return "Ok", 200

# return a random string of FILE_ID_LENGTH length
def gen_id():
  chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
  return "".join(random.SystemRandom().choice(chars) for _ in range(FILE_ID_LENGTH))

# return a file corresponding to a given id. token required
@app.route("/get_file", methods=["GET"])
def get_file():
  data = flask.request.get_json()
  # json
  if not data:
    return "No json", 400
  # token
  if data.get("token", None) != token:
    return "Invalid token", 400
  # ID
  id_ = data.get("id", None)
  if not id_:
    return "No ID", 400
  file = File.query.filter_by(id=id_).first()
  if not file:
    return "Invalid ID", 400
  return flask.send_file(file.full_path()), 200


#######
# Run #
#######

if __name__ == "__main__":
  empty_folder(UPLOAD_FOLDER)
  db.drop_all()
  db.create_all()
  app.run(host=HOST, port=PORT, debug=DEBUG)


