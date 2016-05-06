#-------------------------------------------------------------------------------
# Name:        Google Places API Nearby Request
# Purpose:      USC SSI Master's Thesis Project
#                   Food access in Los Angeles
# Author:      CMH
#
# Created:     06/03/2016
# Copyright:   (c) CMH 2016
# Licence:     Attribution-NonCommercial-ShareAlike 4.0 International
#-------------------------------------------------------------------------------

# Import all of the libraries
import httplib
import urllib
import json
import pprint

#Yelp Python Client Support
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key='NLz9tZJ465VfGE1ZF4wSvw',
    consumer_secret='hPmTpTwFLNskvTNO-lu4HUNskMo',
    token='HLBajJ7AO9-EVkz-eRiaD0DDfFz4kE1q',
    token_secret='RLEhQPqvobQ9umvCKiCN_wJxFHc'
)

yelpClient = Client(auth)


def yelpit( lat, lng, types, offset ):
    #This funciton pulls business data from the Yelp API

    params = {
        'term': 'food',
        'radius_filter': '1500',
        'offset': offset,
        'sort': '0',
        'category_filter': types
    }
    response =  yelpClient.search_by_coordinates(lat,lng,**params)
    #print response.total
    for key in response.businesses:
        print key.location.coordinate.latitude, ",",
        print key.location.coordinate.longitude, ",",
        print key.name, ",",
        print key.categories[0][1], ",",
        print key.rating, ",",
        print key.review_count


    offset += 20
    #print offset, "\n"
    if offset < response.total:
        yelpit(lat, lng, types, offset)

def deets(bus_id):
    conn = httplib.HTTPSConnection("maps.googleapis.com")
    APIkey = "AIzaSyB864Llir0-1NrFaQ1yr3TIzG9fB09IP7c"
    reqstring = "/maps/api/place/details/json?placeid=" + bus_id + "&key=" + APIkey
    #print reqstring
    conn.request("GET", reqstring)
    response = conn.getresponse()
    #print response.status, response.reason
    if response.status == 200:

        # Get and print the actual data
        data = response.read()

        # parse the json into a more useful data structure
        parsed_json = json.loads(data)
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(parsed_json)
        if "rating" in data:
            print parsed_json['result']['rating'], ",",
        else:
            print "0,",
        if "user_ratings_total" in data:
            print parsed_json['result']['user_ratings_total']
        else:
            print "0"

    conn.close()

def googit(lat, lng, types, next_page_token = None):
    conn = httplib.HTTPSConnection("maps.googleapis.com")

    #headers = {"":""}
    #Lat Long for center of census tract
    #lat = "34.0465960"
    #lng = "-118.2515835"

    radius = "1500"
    #types = "restaurant"
    #types = "grocery_or_supermarket"
    APIkey = "AIzaSyB864Llir0-1NrFaQ1yr3TIzG9fB09IP7c"

    if next_page_token is None:
        conn.request("GET", "/maps/api/place/nearbysearch/json?location=" + lat + "," + lng + "&radius=" + radius + "&types=" + types + "&key=" + APIkey)
    else:
        conn.request("GET", "/maps/api/place/nearbysearch/json?location=" + lat + "," + lng + "&radius=" + radius + "&key=" + APIkey + "&pagetoken=" + next_page_token)

    # Get the response and print the response information eg. 200 OK or 404 Not Found
    response = conn.getresponse()
    #print response.status, response.reason

    if response.status == 200:

        # Get and print the actual data
        data = response.read()

        # parse the json into a more useful data structure
        parsed_json = json.loads(data)

        # Load the pretty printer so that we can better see the structure of the data
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(parsed_json)
        #pp.pprint(parsed_json['pagination'])
        #pp.pprint(parsed_json['meta'])
        #pp.pprint(parsed_json['results'])
        #pp.pprint(data)
        #json.dumps( parsed_json, sort_keys=True, indent=4, separators=(',', ': ') )

        items = parsed_json['results']
        for item in items:
            #theLine = ""
            try:

                #print item['place_id']
                #pp.pprint(item)
                print item['geometry']['location']['lat'], ",",
                #theLine = theLine + item['location']['latitude'] + ","
                print item['geometry']['location']['lng'], ",",
                #theLine = theLine + item['location']['longitude'] + ","
                print item['name'], ",",
                print item['types'][0], ",",
                deets(item['place_id'])
                #print ""
                #theLine = theLine + item['link'] + ","
                #print item['images']['standard_resolution']['url']
                #theLine = item['location']['latitude']
                #theLine = theLine + item['location']['latitude'] + "," #+ item['location']['longitude'] + "," + item['link'] + "," + item['images']['standard_resolution']['url'] + "\n"
                #print theLine
                #print (",")
                #print "\n"
                #f.write(theLine)
            except TypeError:
                print ",type error"
                pass
            except KeyError:
                print ",key error"
                pass
        # Close the connection
        #f.close()
        conn.close()

        if "next_page_token" in data:
            #print "recurse"
            #print parsed_json['next_page_token']
            googit(lat,lng,types,parsed_json['next_page_token'])

print "lat, long, name, type, rating, review_count"
#googit("34.1929284","-118.1988009","grocery_or_supermarket");
#yelpit("34.1929284","-118.1988009","grocery,convenience",0);

googit("34.0304827","-118.2686569","grocery_or_supermarket");
#yelpit("34.0304827","-118.2686569","grocery,convenience",0);
