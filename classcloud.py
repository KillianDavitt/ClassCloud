#!/usr/bin/python3
""" Main ClassCloud views, define endpoints
"""
import os
import random
import shutil
import string
import werkzeug
import flask
import flask_sqlalchemy


DIRECTORY = os.path.dirname(os.path.realpath(__file__))

HOST = "127.0.0.1"
PORT = 8000
DEBUG = True
TOKEN_PATH = os.path.join(DIRECTORY, "classcloud.token")
UPLOAD_FOLDER = os.path.join(DIRECTORY, "files")
FILE_ID_LENGTH = 10

# Return token or None.
def get_token():
  with open(TOKEN_PATH) as f:
    return f.read().strip()

# Setup the flask app, db and token.
app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///classcloud.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = flask_sqlalchemy.SQLAlchemy(app)
token = get_token()

# Delete all files and subdirectories of the given folder.
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

# Routes #
##########

# list all files.
@app.route("/list_files", methods=["POST"])
def list_files():
  data = flask.request.values
  if not data:
    return "No token", 400
  if data.get("token", None) != token:
    return "Invalid token", 400
  files = [{file.relative_path() : file.id } for file in File.query.all()]
  #files.sort(key=lambda x: x[1]) # sort by full path
  print(flask.jsonify(files=files).data)
  return flask.jsonify(files), 200

# upload a file, returns the file ID on success
@app.route("/put_file", methods=["POST"])
def put_file():
  data = flask.request.values
  # json
  if not data:
    return "No json", 400
  # token
  if data.get("token", None) != token:
    return "Invalid token", 400
  # path
  path = data.get("path", None)
  if path == None:
    return "No path", 400
  # file data
  fp = flask.request.files.get("file", None)
  if not fp:
    return "No file", 400
  # filename
  filename = werkzeug.secure_filename(fp.filename)
  # check if already exists
  print(filename)
  if File.query.filter_by(path=path, filename=filename).first():
    return "File already exists", 400
  # new File object
  file = File(gen_id(), path, filename)
  # create directories in path and create file
  try:
    os.makedirs(os.path.dirname(file.full_path()), exist_ok=True)
    fp.save(file.full_path())
  except Exception as e:
    print("Could not create file: %r" % e)
    return "Could not create file.", 400
  # save File to database
  db.session.add(file)
  db.session.commit()
  print("File is now in the database")
  return file.id, 200

# return a random string of FILE_ID_LENGTH length
def gen_id():
  chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
  return "".join(random.SystemRandom().choice(chars) for _ in range(FILE_ID_LENGTH))

# return a file corresponding to a given id. token required
@app.route("/get_file/<id>", methods=["GET"])
def get_file(id):
  file = File.query.filter_by(id=id).first()
  if not file:
    return "Invalid ID", 400
  return flask.send_file(file.full_path()), 200

# Remove a file. Token required.
@app.route("/rm_file", methods=["POST"])
def rm_file():
  data = flask.request.values
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
  # remove file and database entry
  os.remove(file.full_path())
  db.session.delete(file)
  db.session.commit()
  # remove empty folders in file path
  path = "".join(file.relative_path().split("/")[:-1]) # remove filename part
  while path:
    os.rmdir(os.path.join(UPLOAD_FOLDER, path))
    path = "".join(path.split("/")[:-1]) # remove deleted folder
  return "Succesfully removed.", 200

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

  def relative_path(self):
    return os.path.join(self.path, self.filename)


#######
# Run #
#######

if __name__ == "__main__":
  db.create_all()
  app.run(host=HOST, port=PORT, debug=DEBUG)
