import googlemaps
from datetime import datetime
import requests
import yaml
import json
import csv
import os
import time



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
        params = {'address': address, 'key': self.APIKey}
        response = requests.get(ENDPOINT, params=params)

        code = response.json()['results'][0]['geometry']['location']
        return str(code['lat']) + ',' + str(code['lng'])


    def get_details(self, place_id):
        ENDPOINT = 'https://maps.googleapis.com/maps/api/place/details/json'
        params = {'key': self.APIKey, 'placeid': place_id}
        response = requests.get(ENDPOINT, params=params).json()

        try:
            phone_number = response['result']['international_phone_number']
        except KeyError:
            phone_number = None
        try:
            website = response['result']['website']
        except KeyError:
            website = None

        result = {
            'phone_number': phone_number,
            'website': website
        }
        return result



    def places(self, query, location, radius):
        ENDPOINT = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        params = {
            'key': self.APIKey,
            'location': self.geocode(location),
            'radius': radius,
            'query': query
        }
        
        results = []
        while True:
            places = requests.get(ENDPOINT, params=params).json()
            results = results + places['results']
            try:
                next_page_token = places['next_page_token']
            except KeyError:
                break
            params['pagetoken'] = next_page_token
            time.sleep(2)

        parsed = []
        for result in results:
            try:
                rating = result['rating']
            except KeyError:
                rating = None

            entry = {
                'id': result['place_id'],
                'name': result['name'],
                'geocode': str(result['geometry']['location']['lat']) + ',' + str(result['geometry']['location']['lng']),
                'rating': rating,
                'address': result['formatted_address']
            }
            entry.update(self.get_details(entry['id']))
            parsed.append(entry)

        return parsed



def save(listings):
    with open('listings.csv', 'w', newline='') as csvfile:
        fieldnames = ['listingId', 'businessName', 'ratingCount', 'averageRating', 'city', 'state', 'zip', 'phone', 'moreInfoURL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

        writer.writeheader()
        for listing in listings:
            writer.writerow(listing)


def main():
    gmaps = GMaps()
    # query = input('[*] Search term: ')
    # location = input('[*] Location: ')
    # radius = int(input('[*] Radius (in meters): '))
    # try:
    #     minRating = float(input('[*] Minimum rating (optional): '))
    # except TypeError:
    #     minRating = None
    # try:
    #     maxRating = float(input('[*] Maximum rating (optional): '))
    # except TypeError:
    #     maxRating = None
    
    # listings = gmaps.places(query, location, radius)
    listings = gmaps.places('nail salon', 'new york', 100)
    print(len(listings))
    print(json.dumps(listings, indent=2))
    # print(json.dumps(listings, indent=2))
    # save(listings)
    # print()
    # print('[*] {} listings scraped. Saved in listings.csv'.format(len(listings)))



if __name__=='__main__':
    main()
