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


jinja_env = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

FormClass = model_form(model.StoredItem, wtforms.form.Form, exclude=["_class"])

class MainHandler(webapp2.RequestHandler):
  def get(self):
    #model.Jar(name='marmalade').put()
    #model.FreshSoul(name='ash').put()
    
    things = model.StoredItem().all().order('-quantity')
    template = jinja_env.get_template('list.html')
    self.response.write(template.render({'list': things}))
    return

class ItemHandler(webapp2.RequestHandler):
  """Handle the adding and displaying of items."""
  def get(self):
    (unused, op, t) =  self.request.path.split("/", 2)
      
    # TODO: sanity check the above type
    q = model.StoredItem().get(t)
    q = FormClass(None, q)
    template = jinja_env.get_template("edit.html")
    if q:
      # we got a key name. editing.
      self.response.write(template.render({'object': q}))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/edit.*', ItemHandler),
], debug=True)
