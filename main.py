from google.appengine.ext import ndb

import webapp2
import json


# Models: boat
class Boat(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    length = ndb.FloatProperty(required=True)
    is_at_sea = ndb.BooleanProperty()


class Fish(ndb.Model):
    name = ndb.StringProperty(required=True)
    ph_min = ndb.FloatProperty()
    ph_max = ndb.FloatProperty()


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, MainPage!')


class BoatHandler(webapp2.RequestHandler):
    def post(self):
        boat_data = json.loads(self.request.body)
        if "name" in boat_data and "type" in boat_data and "length" in boat_data:
            new_boat = Boat(name=boat_data["name"], type=boat_data["type"], length=float(boat_data["length"]))
            new_boat.is_at_sea = True
            new_boat.put()
            new_boat.id = new_boat.key.urlsafe()
            new_boat.put()
            boat_dict = new_boat.to_dict()
            self.response.write(json.dumps(boat_dict))
        else:
            self.response.write('input parameter error')
            self.response.set_status(422)

    def get(self, id=None):
        if id:
            boat = ndb.Key(urlsafe=id).get()
            if boat is not None:
                boat_dict = boat.to_dict()
                self.response.write(json.dumps(boat_dict))
            else:
                self.response.write('can not find boat')
                self.response.set_status(404)


class FishHandler(webapp2.RequestHandler):
    def post(self):
        fish_data = json.loads(self.request.body)
        new_fish = Fish(name=fish_data["name"])
        new_fish.ph_min = fish_data["ph_min"]
        new_fish.ph_max = fish_data["ph_max"]
        new_fish.put()
        fish_dict = new_fish.to_dict()
        fish_dict["self"] = '/fish/' + new_fish.key.urlsafe()
        self.response.write(json.dumps(fish_dict))

    def get(self, id=None):
        if id:
            f = ndb.Key(urlsafe=id).get()
            f.ph_min = 100.0
            f.ph_max = 200.0
            f.put()
            f_d = f.to_dict()
            f_d["self"] = "/fish/" + id
            self.response.write(json.dumps(f.to_dict()))


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/fish', FishHandler),
    ('/fish/(.*)', FishHandler),
    ('/boat', BoatHandler),
    ('/boat/(.*)', BoatHandler)
], debug=True)