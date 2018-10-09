'''
Master post request function that can be used throughout repo

1.) Sends a post request to the orders V2 endpoint
2.) Checks the response
3.) Downloads imagery

Helpful links:
https://planet-platform.readme.io/docs/api-examples#section-order-state
'''

import requests
import json
import time
import os
from requests import Session

#send post request
def make_request(api_key, payload):

    print("making request")
    v2_url = "https://api.planet.com/compute/ops/orders/v2/"

    planet = Session()
    planet.auth = (api_key, "")

    response = planet.post(v2_url, json=payload)

    results = response.json()

    #results link
    response_id = results['id']
    print(response_id)
    order_status_url = "https://api.planet.com/compute/ops/orders/v2" + "/{}".format(response_id)
    results_links = [order_status_url]
    print(results_links)

    return planet, results_links


def check_response(planet, order_urls):

    for order_url in order_urls:
        response = planet.get(order_url)
        print(response.status_code)
        order = response.json()


        while order['state'] == 'running' or order['state'] == 'initializing':
            time.sleep(10)
            response = planet.get(order_url)
            order = response.json()
            print("Order state still running {}".format(order['id']))

            if order["state"] == "success":
                print("success!")
                results_link = order["_links"]["results"]
                order_name = order["name"]
                print("results_link:  {}".format(results_link))
                return results_link, order_name

        if order['state'] == 'failed':
            print("Order failed {}".format(order['id']))
            raise

        elif order['state'] == 'partial':
            print("order partially succeeded {}".format(order['id']))


def download_results(planet, results, order_name, download_path):

    download_links = []
    files = []

    for result in results:
        if '.tif' in result['name'] and 'udm' not in result['name']:
            download_links.append(result['location'])

    for link in download_links:
        res = planet.get(link, stream=True)

        fn = res.url.split("?")[0].split("/")[-1].split(".tif")

        full_fn = download_path + fn[0] + "_" + order_name + '.tif'
        if os.path.exists(full_fn):
            print("{} already exists, skipping".format(full_fn))
            continue

        print("Downloading to: {}".format(full_fn))

        with open(full_fn, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()

        files.append(full_fn)

    print("here are the files: {}".format(files))
    return files
