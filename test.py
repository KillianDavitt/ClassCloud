import classcloud
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
    # invalid token
    result = self.client.get("/list_files")
    self.assertEqual(result.status_code, 400)

  def test_put_file(self):
    post_data = dict(token="hjdh34", file=(StringIO('my file contents'), 'helloworld.txt'), path="/john")
    result = self.client.post('/put_file', data=post_data, content_type="application/json")
    print(result)

if __name__ == "__main__":
  token = classcloud.get_token()
  unittest.main()
