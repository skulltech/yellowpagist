import requests
import yaml
import json
import csv



class YP:
    def __init__(self, APIKey=None):
        if not APIKey:
            with open('creds.yaml') as file:
                creds = yaml.load(file)
            APIKey = creds['YP']['APIKey']
        self.APIKey = APIKey


    def search(self, term, location, radius):
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

        return listings


def main():
    yp = YP()
    term = input('[*] Search term: ')
    location = input('[*] Location: ')
    radius = int(input('[*] Radius (in miles): '))
    
    fieldnames = ['listingId', 'businessName', 'ratingCount', 'averageRating', 'city', 'state', 'zip', 'phone', 'moreInfoURL']
    listings = yp.search(term, location, radius)

    with open('listings.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

        writer.writeheader()
        for listing in listings:
            writer.writerow(listing)

    print()
    print('[*] {} listings scraped. Saved in listings.csv'.format(len(listings)))



if __name__=='__main__':
    main()
