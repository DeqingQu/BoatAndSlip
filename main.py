from google.appengine.ext import ndb
import datetime
import webapp2
import json


from boats import BoatsHandler
from slips import SplitsHandler


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, MainPage!')


class ArrivalHandler(webapp2.RequestHandler):
    def put(self, boat_id=None, slip_id=None):
        if boat_id and slip_id:
            #   get boat entity
            boat_key = ndb.Key(urlsafe=boat_id)
            boat = boat_key.get()
            #   get slip entity
            slip_key = ndb.Key(urlsafe=slip_id)
            slip = slip_key.get()
            #   check current_boat of slip
            if slip.current_boat is None:
                boat.at_sea = False
                slip.current_boat = boat.id
                slip.arrival_date = datetime.datetime.now().strftime("%m/%d/%Y")
                slip_dict = slip.to_dict()
                boat.put()
                slip.put()
                self.response.set_status(200)
                self.response.write(json.dumps(slip_dict))
                return
            else:
                self.response.set_status(403)
        else:
            self.response.set_status(404)


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boats/(.*)/(.*)', BoatsHandler),
    ('/boats/(.*)', BoatsHandler),
    ('/boats', BoatsHandler),
    ('/slips/(.*)', SplitsHandler),
    ('/slips', SplitsHandler),
    ('/arrival/(.*)/(.*)', ArrivalHandler)
], debug=True)