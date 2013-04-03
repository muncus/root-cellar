# Models for things i keep in my root cellar.
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.api import users


class StoredItem(polymodel.PolyModel):
  """ Placeholder object for messing about."""
  name = db.StringProperty()
  rating = db.RatingProperty() # 1-100
  quantity = db.IntegerProperty(default=0)
  notes = db.TextProperty()

class FreshSoul(StoredItem):
  pass

class Wine(StoredItem):
  varietal = db.StringProperty()

class Jar(StoredItem):
  prepared = db.DateProperty(auto_now_add=True)

TYPES = {
    'Jar': Jar,
    'Wine': Wine,
    'Soul': FreshSoul
}

