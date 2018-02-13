import requests
import yaml
import json
import csv
import os



class YP:
    def __init__(self, APIKey=None):
        if not APIKey:
            if 'YPAPIKey' in os.environ:
                APIKey = os.environ['YPAPIKey']
            else:    
                with open('creds.yaml') as file:
                    creds = yaml.load(file)
                APIKey = creds['YP']['APIKey']
        self.APIKey = APIKey


    def search(self, term, location, radius, minRating=None, maxRating=None):
        listings = []
        endpoint = 'http://api2.yp.com/listings/v1/search'
        payload = {
            'key': self.APIKey,
            'term': term,
            'searchloc': location,
            'phonesearch': False,
            'listingcount': 50,
            'shorturl': True,
            'format': 'json',
            'pagenum': 1,
            'radius': radius
        }

        while True:
            response = requests.get(endpoint, params=payload)
            if response.ok:
                response = response.json()
            else:
                break
            if not response['searchResult']['searchListings']:
                break

            listings = listings + response['searchResult']['searchListings']['searchListing']
            payload['pagenum'] = payload['pagenum'] + 1

        if minRating:
            listings =  [x for x in listings if x['averageRating'] >= minRating]
        if maxRating:
            listings =  [x for x in listings if x['averageRating'] <= maxRating]
        
        return listings


def save(listings, filename):
    with open('listings/' + filename, 'w', newline='') as csvfile:
        fieldnames = ['listingId', 'businessName', 'ratingCount', 'averageRating', 'city', 'state', 'zip', 'phone', 'moreInfoURL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

        writer.writeheader()
        for listing in listings:
            writer.writerow(listing)


def main():
    yp = YP()
    term = input('[*] Search term: ')
    location = input('[*] Location: ')
    radius = int(input('[*] Radius (in miles): '))
    try:
        minRating = float(input('[*] Minimum rating (optional): '))
    except TypeError:
        minRating = None
    try:
        maxRating = float(input('[*] Maximum rating (optional): '))
    except TypeError:
        maxRating = None
    
    listings = yp.search(term, location, radius, minRating, maxRating)
    save(listings, 'listings.csv')
    print()
    print('[*] {} listings scraped. Saved in listings.csv'.format(len(listings)))



if __name__=='__main__':
    main()
