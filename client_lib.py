import requests
import urllib.parse


# Return a file with given ID from the file server.
def get_file(url, token, id_):
  url = urllib.parse.urljoin(url, "/get_file")
  data = {"token": token, "id": id_}
  response = requests.get(url, json=data)
  print(response.text)
  return response.content


# Return a list of (file IDs, file paths) from the file server.
def list_files(url, token):
  url = urllib.parse.urljoin(url, "/list_files")
  response = requests.get(url, json={"token": token})
  print(response.text)
  return response.json()["files"]


# Upload a file to the file server, return True on success else False.
def put_file(url, token, path, filename, file_bytes):
  url = urllib.parse.urljoin(url, "/put_file")
  files = {"file": (filename, file_bytes)}
  data = {"token": token, "path": path}
  response = requests.post(url, files=files, data=data)
  print(response.text)
  return response.status_code == 200

# Remove a file from the file server, return True on success else False.
def rm_file(url, token, id):
  url = urllib.parse.urljoin(FILE_SERVER_URL, "/rm_file")
  data = {"token": token, "id": id_}
  response = requests.post(url, files=files, data=data)
  print(response.text)
  return response.status_code == 200