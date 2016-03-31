import classcloud
import unittest

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

if __name__ == "__main__":
  token = classcloud.get_token()
  unittest.main()