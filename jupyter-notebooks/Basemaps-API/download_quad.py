#packages
import os
import json
import requests
import config
import urllib.request

#setup Planet API key <= I put mine in a config file

#setup Planet base URL
API_URL = "https://api.planet.com/basemaps/v1/mosaics"

#setup session
session = requests.Session()

#authenticate
session.auth = (config.PLANET_API_KEY, "")

#set params for search using name of mosaic
parameters = {
    "name__is" :"nsw_ps_1month_date_ramp_L15_mosaic"
}

#make get request to access mosaic from basemaps API
res = session.get(API_URL, params = parameters)

#response status code
print(res.status_code)

#print metadata for mosaic
mosaic = res.json()
print(json.dumps(mosaic, indent=2))

#get id
mosaic_id = mosaic['mosaics'][0]['id']

#get bbox for entire mosaic
mosaic_bbox = mosaic['mosaics'][0]['bbox']

print(mosaic_id)
print(mosaic_bbox)

#converting bbox to string for search params
string_bbox = ','.join(map(str, mosaic_bbox))

#search for mosaic quad using AOI
search_parameters = {
    'bbox': string_bbox,
    'minimal': True
}

#accessing quads using metadata from mosaic
quads_url = "{}/{}/quads".format(API_URL, mosaic_id)

#send request
res = session.get(quads_url, params=search_parameters, stream=True)

quads = res.json()
items = quads['items']

#iterate over quad download links and saving to folder by id
for i in items:
    link = i['_links']['download']
    name = i['id']
    name = name + '.tiff'
    DIR = 'quads/'
    filename = os.path.join(DIR, name)

    if not os.path.isfile(filename):
        urllib.request.urlretrieve(link, filename)
