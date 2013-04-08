#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import os
import webapp2
import logging

import model
import wtforms
from wtforms.ext.appengine.db import model_form

from google.appengine.api.datastore_errors import BadKeyError


jinja_env = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

FormClass = model_form(model.StoredItem, wtforms.form.Form, exclude=["_class"])
FORMS = {}
for cls in model.TYPES.keys():
  FORMS[cls] = model_form(model.TYPES[cls], wtforms.form.Form, exclude=["_class"])

class MainHandler(webapp2.RequestHandler):
  def get(self):
    #model.Jar(name='marmalade').put()
    #model.FreshSoul(name='ash').put()
    
    things = model.StoredItem().all().order('-quantity')
    template = jinja_env.get_template('list.html')
    self.response.write(template.render({
        'list_title': "Current Contents",
        'list': things}))
    return

class ItemHandler(webapp2.RequestHandler):
  """Handle the adding and displaying of items."""

  def showItemList(self):
    """Display a list of available types. for use when adding an item."""
    template = jinja_env.get_template("typelist.html")
    v = {
      'list_title': "Choose a type to add",
      'list': model.TYPES}
    self.response.write(template.render(v))
    return

  def editItem(self, itemform, title=None):
    """Show an item's edit form."""
    # XXX: switch to using item here?
    if not title:
      title = "Edit Item: %s" % itemform.name.data

    template = jinja_env.get_template("edit.html")
    self.response.write(template.render({
        'object': itemform,
        'formtitle': title}))

  def get(self, key=None):
    if not key:
      # adding a new item, present list of types.
      self.showItemList()
      return
    if key in model.TYPES.keys():
      logging.debug("Adding new item.")
      # create a new object.
      q = model.TYPES[key]()
      q = FORMS[key](None, q)
      title = "Add new item: %s" % key
      self.editItem(q, title=title)
    else:
      logging.debug("editing item.")
      q = model.StoredItem().get(key)
      q = FormClass(None, q)
      self.editItem(q)

  def post(self, key):
    form = FormClass(self.request.POST)
    if form.validate():
      item = None
      try:
        item = model.StoredItem().get(key)
        form.populate_obj(item)
        item.put()
      except(BadKeyError):
        # no such key, create new entry.
        item = model.StoredItem()
        form.populate_obj(item)
        item.put()
        self.redirect("/edit/%s" % item.key())
        return
      # show the item we just edited.
      return self.get(key)
    else:
      logging.debug("form input did not validate!")
      logging.debug(form.errors)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/edit/(.*)', ItemHandler),
    ('/add', ItemHandler),
    ('/add/(.*)', ItemHandler),
], debug=True)
