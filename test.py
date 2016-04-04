import classcloud
import flask
import json
import io
import os
import unittest

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TESTING_DB = "classcloud_testing.sqlite"

token = classcloud.get_token()
with open("test.txt", "rb") as f:
  text_bytes = f.read()
with open("test.pdf", "rb") as f:
  pdf_bytes = f.read()
def put_text():
  return {"file": (io.BytesIO(text_bytes), "test.txt"), "token": token, "path": "john"}
def put_pdf():
  return {"file": (io.BytesIO(pdf_bytes), "test.pdf"), "token": token, "path": "john"}

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
    self.assertEqual(result.data, b"No token")
    # invalid token
    result = self.client.get("/list_files", data=json.dumps({"token": "invalid_token"}), content_type="application/json")
    self.assertEqual(result.status_code, 400)
    self.assertEqual(result.data, b"Invalid token")
    # correct token
    result = self.client.get("/list_files", data=json.dumps({"token": token}), content_type="application/json")
    self.assertEqual(result.status_code, 200)
    files = flask.json.loads(result.data)["files"]
    self.assertEqual(len(files), 0)
    # list_files contains uploaded file
    self.client.post("/put_file", data=put_text())
    result = self.client.get("/list_files", data=json.dumps({"token": token}), content_type="application/json")
    self.assertEqual(result.status_code, 200)
    files = flask.json.loads(result.data)["files"]
    self.assertTrue(any([file[1].split("/")[-1] == "test.txt" for file in files]))
    self.assertEqual(len(files), 1)

  def test_get_file(self):
    # invalid token
    result = self.client.get("/get_file", data=json.dumps({"token": ""}), content_type="application/json")
    self.assertEqual(result.status_code, 400)
    self.assertEqual(result.data, b"Invalid token")
    # upload text file and get ID
    self.client.post("/put_file", data=put_text())
    result = self.client.get("/list_files", data=json.dumps({"token": token}), content_type="application/json")
    id_ = flask.json.loads(result.data)["files"][0][0]
    # invalid ID
    get_data = json.dumps({"id": id_ + "incorreect", "token": token})
    result = self.client.get("/get_file", data=get_data, content_type="application/json")
    self.assertEqual(result.status_code, 400)
    self.assertEqual(result.data, b"Invalid ID")
    # verify text file
    get_data = json.dumps({"id": id_, "token": token})
    result = self.client.get("/get_file", data=get_data, content_type="application/json")
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.data, text_bytes)

  def test_get_file_pdf(self):
    # upload PDF and get ID
    self.client.post("/put_file", data=put_pdf())
    result = self.client.get("/list_files", data=json.dumps({"token": token}), content_type="application/json")
    id_ = flask.json.loads(result.data)["files"][0][0]
    # verify PDF
    get_data = json.dumps({"id": id_, "token": token})
    result = self.client.get("/get_file", data=get_data, content_type="application/json")
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.data, pdf_bytes)
    with open("result_pdf.pdf", "wb") as f:
        f.write(result.data)
    with open("result_pdf.pdf", "rb") as f:
        self.assertEqual(result.data, f.read())
    os.remove("result_pdf.pdf")

  def test_put_file(self):
    # upload simple text file
    result = self.client.post("/put_file", data=put_text())
    self.assertEqual(result.status_code, 200)
    # duplicate file
    result = self.client.post("/put_file", data=put_text())
    self.assertEqual(result.status_code, 400)
    # upload PDF
    result = self.client.post("/put_file", data=put_pdf())
    self.assertEqual(result.status_code, 200)

  def test_rm_file(self):
    # upload simple text file
    result = self.client.post("/put_file", data=put_text())
    # list of files
    result = self.client.get("/list_files", data=json.dumps({"token": token}), content_type="application/json")
    files = flask.json.loads(result.data)["files"]
    self.assertEqual(len(files), 1)
    # rm file
    result = self.client.post("/rm_file", data=json.dumps({"token": token, "id": files[0][0]}), content_type="application/json")
    self.assertEqual(result.status_code, 200)
    # list of files
    result = self.client.get("/list_files", data=json.dumps({"token": token}), content_type="application/json")
    files = flask.json.loads(result.data)["files"]
    self.assertEqual(len(files), 0)


  def tearDown(self):
    os.remove(os.path.join(DIRECTORY, TESTING_DB))

if __name__ == "__main__":
    unittest.main()