from flask import Flask, request, render_template, make_response
from flask.ext.restful import Api, Resource, reqparse

import json
import string
import random
from datetime import datetime

# define our categories
CATEGORIES = ( 'shop', 'restaurant', 'bar', 'club' )

# load business data from disk, load into dictionary (key/value)
with open('businesses.json') as data:
    businesses = json.load(data)
with open('events.json') as data:
    events = json.load(data)

#
# define some helper functions
#
def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def error_if_business_not_found(business_id):
    if business_id not in businesses:
        message = "Business {} doesn't exist".format(business_id)    
        abort(404, message)

def error_if_event_not_found(event_id):
    if event_id not in events:
        message = "Event {} doesn't exist".format(event_id)
        abort(404, message)


def render_business_as_html(business):
    return render_template(
        'business.html',
         business=business,
         categories=CATEGORIES)

def render_business_list_as_html(businesses):
    return render_template(
        'businesses.html',
        businesses=businesses,
        categories=CATEGORIES)

def render_event_as_html(event):
    return render_template(
        'event.html',
        event=event)
        
def render_event_list_as_html(events):
    return render_template(
        'events.html',
        events=events)

def nonempty_string(x):
    s = str(x)
    if len(x) == 0:
        raise ValueError('string is empty')
    return s

#
# specify the data we need to create a new help request
#
new_business_parser = reqparse.RequestParser()
for arg in ['name', 'location', 'URL', 'phone', 'hours', 'rating', 'description', 'category']:
    new_business_parser.add_argument(
       arg, type=nonempty_string, required=True,
       help="'{}' is a required value".format(arg))

new_event_parser = reqparse.RequestParser()
for arg in ['name', 'location', 'venue', 'URL', 'date', 'time', 'description']:
    new_event_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))

#
# specify the data we need to update an existing help request
#
#
update_business_parser = reqparse.RequestParser()
update_business_parser.add_argument(
    'name', type=str)
update_business_parser.add_argument(
    'location', type=str)
update_business_parser.add_argument(
    'URL', type=str)
update_business_parser.add_argument(
    'phone', type=str)
update_business_parser.add_argument(
    'hours', type=str)
update_business_parser.add_argument(
    'rating', type=str)
update_business_parser.add_argument(
    'description', type=str)
update_business_parser.add_argument(
    'category', type=str)


update_event_parser = reqparse.RequestParser()


#
# specify the parameters for filtering and sorting help requests
#
query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'q', type=str, default='')

query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'q', type=str, default='')

#
# define our (kinds of) resources
#
class Business(Resource):
    def get(self, business_id):
        error_if_business_not_found(business_id)
        return make_response(
            render_business_as_html(businesses[business_id]), 200) #gives the (a dictionary) we need 2 lists and two single item class definitions; start by just implementing GET methods

    def patch(self, business_id):
        error_if_business_not_found(business_id)
        business=businesses[business_id]
        update = update_business_parser.parse_args()
        business['name']= update['name']
        business['location'] = update['location']
        business['URL'] = update['URL']
        business['phone'] = update['phone']
        business['hours'] = update['hours']
        business['rating'] = update['rating']
        business['description'] = update['description']
        business['category'] = update['category']
        return make_response(
            render_business_as_html(business), 200)

class Event(Resource):
    def get(self, event_id):
        error_if_event_not_found(event_id)
        return make_response(
            render_event_as_html(events[event_id]), 200)
            
    def patch(self, business_id):
        error_if_event_not_found(event_id)
        event=events[event_id]
        update = update_event_parser.parse_args()
#       event['name'] = update['name']

class BusinessAsJSON(Resource):
    def get(self, business_id):
        error_if_business_not_found(business_id)
        return businesses[business_id]
    
class EventAsJSON(Resource):
    def get(self, business_id):
        error_if_event_not_found(event_id)
        return events[event_id]
        
class BusinessList(Resource):
    def get(self):
        query = query_parser.parse_args()
        return make_response(
            render_business_list_as_html(businesses), 200)

    def post(self): 
        business = new_business_parser.parse_args()
        businesses[generate_id()] = business
        return make_response(
            render_business_list_as_html(businesses), 201)

class EventList(Resource):
    def get(self):
        query = query_parser.parse_args()
        return make_response(
            render_event_list_as_html(events), 200)
                    
    def post(self):
        event = new_event_parser.parse_args()
        events[generate_id()] = event
        return make_response(
            render_event_list_as_html(events), 201)

class BusinessListAsJSON(Resource):
    def get(self):
        return businesses

class EventListAsJSON(Resource):
    def get(self):
        return events
#
# assign URL paths to our resources
#
app = Flask(__name__)
api = Api(app)
api.add_resource(BusinessList, '/businesses')
api.add_resource(BusinessListAsJSON, '/businesses.json')
api.add_resource(Business, '/business/<string:business_id>')
api.add_resource(BusinessAsJSON, '/business/<string:business_id>.json')
api.add_resource(EventList, '/events')
api.add_resource(EventListAsJSON, '/events.json')
api.add_resource(Event, '/event/<string:event_id>')
api.add_resource(EventAsJSON, '/event/<string:event_id>.json')

# start the server
if __name__ == '__main__':
    app.run(debug=True)
