import classcloud
import json
import unittest
from io import StringIO
token = None

class ServerTestCase(unittest.TestCase):

  def setUp(self):
    classcloud.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///classcloud_testing.sqlite"
    classcloud.app.config["TESTING"] = True
    classcloud.db.drop_all()
    classcloud.db.create_all()
    self.client = classcloud.app.test_client()

  def test_list_files(self):
    # no token
    result = self.client.get("/list_files")
    self.assertEqual(result.status_code, 400)
    # invalid token
    result = self.client.get("/list_files", data=json.dumps({"token": token}), content_type="application/json")
    self.assertEqual(result.status_code, 400)

  def test_put_file(self):
    post_data = dict(token=token, file=(StringIO('my file contents'), 'helloworld.txt'), path="/john")
    result = self.client.post('/put_file', data= {'token':token, 'path':'/john', 'file': (StringIO('my file contents'), 'helloworld.txt')})
    print(result)
    print(result.data)

if __name__ == "__main__":
  token = classcloud.get_token()
  unittest.main()
