from google.appengine.ext import ndb
import webapp2
import json


class Slip(ndb.Model):
    id = ndb.StringProperty()
    number = ndb.IntegerProperty(required=True)
    current_boat = ndb.StringProperty(default=None)
    arrival_date = ndb.StringProperty(default=None)
    departure_history = ndb.JsonProperty(default=None)


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
            if slip is not None and key.kind() == "Slip":
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

    def put(self, id=None):
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
                    self.response.write('input parameter error')
                    self.response.set_status(422)
            else:
                self.response.write('can not find slip')
                self.response.set_status(404)

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
                # check whether there is a boat in the slip
                if slip.current_boat is not None:
                    boat_key = ndb.Key(urlsafe=slip.current_boat)
                    boat = boat_key.get()
                    boat.at_sea = True
                    boat.put()
                key.delete()
                self.response.set_status(204)
            else:
                self.response.write('can not find slip')
                self.response.set_status(404)