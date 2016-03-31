import classcloud
import json
import io
import os
import unittest

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TESTING_DB = "classcloud_testing.sqlite"

token = classcloud.get_token()

class ServerTestCase(unittest.TestCase):

  def setUp(self):
    classcloud.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + TESTING_DB
    classcloud.app.config["TESTING"] = True
    classcloud.empty_folder(classcloud.UPLOAD_FOLDER)
    classcloud.db.drop_all()
    classcloud.db.create_all()
    self.client = classcloud.app.test_client()

  def test_list_files(self):
    # no token
    result = self.client.get("/list_files")
    self.assertEqual(result.status_code, 400)
    # invalid token
    result = self.client.get("/list_files", data=json.dumps({"token": "invalid_token"}), content_type="application/json")
    self.assertEqual(result.status_code, 400)
    # correct token
    result = self.client.get("/list_files", data=json.dumps({"token": token}), content_type="application/json")
    self.assertEqual(result.status_code, 200)

  def test_get_file(self):
    # upload simple text file
    data = json.dumps({"token": token, "path": "john", "filename": "test.txt", "file": open("test.txt").read()})
    result = self.client.post("/put_file", data=data, content_type="application/json")
    print(result)
    
    result = self.client.get("/list_files", data=json.dumps({"token": token}), content_type="application/json")
    print(result.data) 
    
    data = json.dumps({'id':'4fsrf4'})
    result = self.client.get("/get_file", data=data, content_type="application/json")
    print(result.data)
    self.assertEqual(result.status_code, 200)

  def test_put_file(self):
    # upload simple text file
    data = json.dumps({"token": token, "path": "john", "filename": "test.txt", "file": open("test.txt").read()})
    result = self.client.post("/put_file", data=data, content_type="application/json")
    self.assertEqual(result.status_code, 200)
    # duplicate file
    result = self.client.post("/put_file", data=data, content_type="application/json")
    self.assertEqual(result.status_code, 400)

  def tearDown(self):
    os.remove(os.path.join(DIRECTORY, TESTING_DB))

if __name__ == "__main__":
  unittest.main()
