class File(db.Model):
  id = db.Column(db.String(), primary_key=True)
  path = db.Column(db.String())
  filename = db.Column(db.String(20))
 
  def __init__(self, id, path, filename):
    self.id = id
    self.path = path
    self.filename = filename
 
