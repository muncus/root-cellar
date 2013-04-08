# Models for things i keep in my root cellar.
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.api import users

from wtforms.ext.appengine.db import model_form


class StoredItem(polymodel.PolyModel):
  """ Placeholder object for messing about."""
  name = db.StringProperty()
  rating = db.RatingProperty(default=0) # 0-100, with 0 being considered unrated.
  quantity = db.IntegerProperty(default=0)
  notes = db.TextProperty()
  
class FreshSoul(StoredItem):
  pass

class Wine(StoredItem):
  varietal = db.StringProperty()

class Jar(StoredItem):
  prepared = db.DateProperty(auto_now_add=True)
  recipe_src = db.StringProperty()

TYPES = {
    'Jar': Jar,
    'Wine': Wine,
    'Soul': FreshSoul
}

