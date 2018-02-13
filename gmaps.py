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



    def places(self, query, location, radius, min_rating=None, max_rating=None):
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
                rating = 0.0

            entry = {
                'id': result['place_id'],
                'name': result['name'],
                'geocode': str(result['geometry']['location']['lat']) + ',' + str(result['geometry']['location']['lng']),
                'rating': rating,
                'address': result['formatted_address']
            }
            entry.update(self.get_details(entry['id']))
            parsed.append(entry)

        if min_rating:
            parsed =  [x for x in parsed if x['rating'] >= min_rating]
        if max_rating:
            parsed =  [x for x in parsed if x['rating'] <= max_rating]
        return parsed



def save(listings, filename):
    with open('listings/' + filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'geocode', 'rating', 'address', 'phone_number', 'website']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

        writer.writeheader()
        for listing in listings:
            writer.writerow(listing)


def main():
    gmaps = GMaps()
    query = input('[*] Search query: ')
    location = input('[*] Location: ')
    radius = int(input('[*] Radius (in meters): '))
    try:
        min_rating = float(input('[*] Minimum rating (optional): '))
    except TypeError:
        min_rating = None
    try:
        max_rating = float(input('[*] Maximum rating (optional): '))
    except TypeError:
        max_rating = None
    
    places = gmaps.places(query, location, radius, min_rating, max_rating)
    save(places, 'listings.csv')
    print()
    print('[*] {} places scraped. Saved in listings.csv'.format(len(places)))



if __name__=='__main__':
    main()
