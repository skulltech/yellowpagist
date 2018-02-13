import googlemaps
from datetime import datetime

import yaml
import json
import csv
import os



class GMaps:
    def __init__(self, APIKey=None):
        if not APIKey:
            APIKey = self.getAPIKey()
        self.APIKey = APIKey


    @staticmethod
    def getAPIKey():
        if 'YPAPIKey' in os.environ:
            APIKey = os.environ['GoogleAPIKey']
        else:    
            with open('creds.yaml') as file:
                creds = yaml.load(file)
            APIKey = creds['Google']['APIKey']
        return APIKey


    def geocode(self, address):
        ENDPOINT = 'https://maps.googleapis.com/maps/api/geocode/json'


def places(query, location, radius, minRating=None, maxRating=None):
    APIKey = getAPIKey()
    gmaps = googlemaps.Client(key=APIKey)
    geocode = gmaps.geocode(location)[0]['geometry']['location']
    places = gmaps.places(query=query, location=geocode, radius=radius)

    results = []
    while True:
        print(len(places['results']))
        results = results + places['results']
        next_page_token = places['next_page_token']
        print(next_page_token)
        print()
        places = gmaps.places(query=query, location=geocode, radius=radius, page_token=next_page_token)

    # if minRating:
    #     listings =  [x for x in listings if x['averageRating'] >= minRating]
    # if maxRating:
    #     listings =  [x for x in listings if x['averageRating'] <= maxRating]
    
    return places


def save(listings):
    with open('listings.csv', 'w', newline='') as csvfile:
        fieldnames = ['listingId', 'businessName', 'ratingCount', 'averageRating', 'city', 'state', 'zip', 'phone', 'moreInfoURL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

        writer.writeheader()
        for listing in listings:
            writer.writerow(listing)


def main():
    query = input('[*] Search term: ')
    location = input('[*] Location: ')
    radius = int(input('[*] Radius (in meters): '))
    # try:
    #     minRating = float(input('[*] Minimum rating (optional): '))
    # except TypeError:
    #     minRating = None
    # try:
    #     maxRating = float(input('[*] Maximum rating (optional): '))
    # except TypeError:
    #     maxRating = None
    
    listings = places(query, location, radius)
    print(json.dumps(listings, indent=2))
    # save(listings)
    # print()
    # print('[*] {} listings scraped. Saved in listings.csv'.format(len(listings)))



if __name__=='__main__':
    main()
