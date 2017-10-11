from google.appengine.ext import ndb

import webapp2
import json


# Models: boat
class Boat(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    length = ndb.FloatProperty(required=True)
    at_sea = ndb.BooleanProperty(default=True)


class Slip(ndb.Model):
    id = ndb.StringProperty()
    number = ndb.IntegerProperty(required=True)
    current_boat = ndb.StringProperty()
    arrival_date = ndb.DateProperty()
    departure_history = ndb.JsonProperty()


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, MainPage!')


class BoatsHandler(webapp2.RequestHandler):
    def post(self):
        boat_data = json.loads(self.request.body)
        if "name" in boat_data and "type" in boat_data and "length" in boat_data:
            new_boat = Boat(name=boat_data["name"], type=boat_data["type"], length=float(boat_data["length"]))
            new_boat.put()
            new_boat.id = new_boat.key.urlsafe()
            new_boat.put()
            boat_dict = new_boat.to_dict()
            self.response.write(json.dumps(boat_dict))
            self.response.set_status(201)
        else:
            self.response.write('input parameter error')
            self.response.set_status(422)

    def get(self, id=None):
        if id:
            key = ndb.Key(urlsafe=id)
            boat = key.get()
            if boat is not None and key.kind() == "Boat":
                boat_dict = boat.to_dict()
                self.response.write(json.dumps(boat_dict))
            else:
                self.response.write('can not find boat')
                self.response.set_status(404)
        else:
            query = Boat.query()
            boats = []
            for boat in query:
                boats.append(boat.to_dict())
            self.response.write(json.dumps(boats))

    def patch(self, id=None):
        if id:
            key = ndb.Key(urlsafe=id)
            boat = key.get()
            #   to check whether the boat with id is existed
            if boat is not None and key.kind() == "Boat":
                body_data = json.loads(self.request.body)
                if "name" in body_data:
                    boat.name = body_data["name"]
                if "type" in body_data:
                    boat.type = body_data["type"]
                if "length" in body_data:
                    boat.length = float(body_data["length"])
                boat.put()
                boat_dict = boat.to_dict()
                self.response.write(json.dumps(boat_dict))
            else:
                self.response.write('can not find boat')
                self.response.set_status(404)

    def delete(self, id=None):
        if id:
            key = ndb.Key(urlsafe=id)
            boat = key.get()
            if boat is not None and key.kind()=="Boat":
                if key.kind() == "Boat":
                    key.delete()
                    self.response.set_status(204)
            else:
                self.response.write('can not find Boat')
                self.response.set_status(404)


class BoatsAtSeaHandler(webapp2.RequestHandler):
    def put(self, id=None):

        if id:

            self.response.write('at_sea')
        else:
            self.response.set_status(404)


class SplitsHandler(webapp2.RequestHandler):
    def post(self):
        slip_data = json.loads(self.request.body)
        if "number" in slip_data:
            new_slip = Slip(number=int(slip_data["number"]))
            new_slip.put()
            new_slip.id = new_slip.key.urlsafe()
            new_slip.put()
            slip_dict = new_slip.to_dict()
            self.response.write(json.dumps(slip_dict))
            self.response.set_status(201)
        else:
            self.response.write('input parameter error')
            self.response.set_status(422)

    def get(self, id=None):
        if id:
            key = ndb.Key(urlsafe=id)
            slip = key.get()
            if key is not None and key.kind() == "Slip":
                slip_dict = slip.to_dict()
                self.response.write(json.dumps(slip_dict))
            else:
                self.response.write('can not find slip')
                self.response.set_status(404)
        else:
            query = Slip.query()
            slips = []
            for slip in query:
                slips.append(slip.to_dict())
            self.response.write(json.dumps(slips))

    def patch(self, id=None):
        if id:
            key = ndb.Key(urlsafe=id)
            slip = key.get()
            #   to check whether the slip with id is existed
            if slip is not None and key.kind() == "Slip":
                body_data = json.loads(self.request.body)
                if "number" in body_data:
                    slip.number = int(body_data["number"])
                slip.put()
                slip_dict = slip.to_dict()
                self.response.write(json.dumps(slip_dict))
            else:
                self.response.write('can not find slip')
                self.response.set_status(404)

    def delete(self, id=None):
        if id:
            key = ndb.Key(urlsafe=id)
            slip = key.get()
            if slip is not None and key.kind() == "Slip":
                key.delete()
                self.response.set_status(204)
            else:
                self.response.write('can not find slip')
                self.response.set_status(404)


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boats/(.*)/at_sea', BoatsAtSeaHandler),
    ('/boats', BoatsHandler),
    ('/boats/(.*)', BoatsHandler),
    ('/slips', SplitsHandler),
    ('/slips/(.*)', SplitsHandler),
], debug=True)