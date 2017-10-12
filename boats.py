from google.appengine.ext import ndb
import datetime
import webapp2
import json

from slips import Slip


# Models: boat
class Boat(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    length = ndb.FloatProperty(required=True)
    at_sea = ndb.BooleanProperty(default=True)


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

    def put(self, boat_id=None):
        if boat_id:
            key = ndb.Key(urlsafe=boat_id)
            boat = key.get()
            #   to check whether the boat with id is existed
            if boat is not None and key.kind() == "Boat":
                body_data = json.loads(self.request.body)
                if "name" in body_data and "type" in body_data and "length" in body_data:
                    boat.name = body_data["name"]
                    boat.type = body_data["type"]
                    boat.length = float(body_data["length"])
                    boat.put()
                    boat_dict = boat.to_dict()
                    self.response.write(json.dumps(boat_dict))
                else:
                    self.response.write('input parameter error')
                    self.response.set_status(422)
            else:
                self.response.write('can not find boat')
                self.response.set_status(404)

    def patch(self, boat_id=None, at_sea=None):
        if boat_id and at_sea == 'at_sea':
            #   get boat entity
            boat_key = ndb.Key(urlsafe=boat_id)
            boat = boat_key.get()
            if boat.at_sea:
                boat_dict = boat.to_dict()
                self.response.write(json.dumps(boat_dict))
                return
            else:
                query = Slip.query()
                arrival_slip = False
                for slip in query:
                    if slip.current_boat == boat.id:
                        arrival_slip = slip
                        break
                if arrival_slip:
                    # update slip info
                    arrival_slip.current_boat = None
                    arrival_slip.arrival_date = None
                    # arrival_slip.departure_history
                    now_date = datetime.datetime.now().strftime("%m/%d/%Y")
                    departure_record = {"departure_date": now_date, "departed_boat": boat.id}
                    if arrival_slip.departure_history is None:
                        arrival_slip.departure_history = [departure_record]
                    else:
                        arrival_slip.departure_history.append(departure_record)
                    arrival_slip.put()
                    # update boat info
                    boat.at_sea = True
                    boat.put()
                    boat_dict = boat.to_dict()
                    self.response.write(json.dumps(boat_dict))
                    return
                else:
                    self.response.write('can not find slip')
                    self.response.set_status(403)
        elif boat_id:
            key = ndb.Key(urlsafe=boat_id)
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
        else:
            self.response.write('can not find Boat or not at sea')
            self.response.set_status(404)