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

  def test_put_file(self):
    #post_data = dict(token=token, file=(StringIO('my file contents'), 'helloworld.txt'), path="/john")
    result = self.client.post('/put_file', data= {'token':token, 'path':'/john', 'file': (io.BytesIO(b"this is a test"), 'test.pdf')})
    print(result)
    print(result.data)

  def tearDown(self):
    os.remove(os.path.join(DIRECTORY, TESTING_DB))

if __name__ == "__main__":
  unittest.main()
