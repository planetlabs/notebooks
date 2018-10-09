'''
Master post request function that can be used throughout repo. Includes
functions to post to data API including:

* Searches and filtering

Helpful links:
https://developers.planet.com/docs/api/
'''
import requests

def quick_search(api_key, and_filter, item_types):
    '''Makes post request to the Search API'''

    #Make the api post request with requests
    if not api_key:
        print("Please add your API request to the operation")

    api_request = "https://api.planet.com/data/v1/quick-search"

    payload = {
        "item_types": item_types,
        "filter": and_filter
    }

    res = requests.post(api_request, auth=(api_key, ''), json=payload)

    return res.json()
