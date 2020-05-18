import os
import requests
import json
import geopandas as gpd
from keplergl import KeplerGl
import pandas as pd
from collections import defaultdict
import holoviews as hv
import hvplot.pandas
import time
from bokeh.models.formatters import DatetimeTickFormatter

hv.extension('bokeh')
xformatter = DatetimeTickFormatter(months='%b %Y')

def jpp(data):
    print(json.dumps(data, indent=4))

def get_subscription_bounds(subscription_id, pl_api_key, sif_env='sif-live'):
    # Setup basic auth session
    BASIC_AUTH = (pl_api_key, '')
    session = requests.Session()
    session.auth=BASIC_AUTH
    
    SIF_BASE_URL = f'https://{sif_env}.prod.planet-labs.com/'
    subscription_get_url = SIF_BASE_URL + f'subscriptions/{subscription_id}'
    
    subs_get_resp = requests.get(
        subscription_get_url, 
        auth=BASIC_AUTH
    )
    # Convert geometry to a Geopandas DataFrame
    subscription_geometry = subs_get_resp.json()['geometry']
    return subscription_geometry

    # subscription_gdf = gpd.GeoDataFrame.from_file(json.dumps(subs_get_resp.json()))

    # # Visualize Geometry with KeplerGL
    # subscription_map = KeplerGl(height=500)
    # subscription_map.add_data(data=subscription_gdf, name=f'Wuhu Ships Subscription {subscription_id}')
    # return subscription_map

def get_stats_geometry_from_widget_selection(subscription_widget, indexed_stats_df, pl_api_key):
    description = subscription_widget
    selection = indexed_stats_df.query('Description == @description')

    subscription_id = selection['Subscription ID'].iloc[0]
    
    sif_env_name = selection['SIF Env'].iloc[0]

    if sif_env_name == 'Live':
        sif_env = 'sif-live'
    else:
        sif_env = 'sif-next'
        
    subscription_geom = get_subscription_bounds(subscription_id, pl_api_key, sif_env=sif_env)
    return subscription_geom

def get_report_data(report_url, pl_api_key):
    # Setup Basic Auth
    BASIC_AUTH = (pl_api_key, '')
    session = requests.Session()
    session.auth=BASIC_AUTH
    
    results_resp = requests.get(
        report_url,
        auth=BASIC_AUTH,
    )
    print(results_resp.status_code)
    return results_resp.json()

def restructure_results(results_json):
    cols = results_json['cols']
    rows = results_json['rows']
    
    records = []
    for r in rows:
        rec = defaultdict()
        for i, cell in enumerate(r):
            rec[cols[i]['label']] = cell
        records.append(rec)
        
    df = pd.DataFrame.from_records(records)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df = df.set_index('Start Time')
    return df

def cloud_normalize_results_df(report_df):
    report_df['Detections by Number of Clear Pixels'] = report_df['Total Object Count'] / report_df['Clear Pixel Count (PSScene4Band-udm2-band_1_count)'] * report_df['Total Pixel Count (PSScene4Band-udm2-total_px_count)']
    # Account for Haze
    report_df['Detections by Number of Clear Pixels - Haze Correction'] = \
        (report_df['Total Object Count'] / \
            report_df['Clear Pixel Count (PSScene4Band-udm2-band_1_count)'] \
            + report_df['Light Haze Pixel Count (PSScene4Band-udm2-band_4_count)'] \
            + (report_df['Heavy Haze Pixel Count (PSScene4Band-udm2-band_5_count)'] /2)) \
            * report_df['Total Pixel Count (PSScene4Band-udm2-total_px_count)'].mean()

        
    # remove data points where (udm2_clear_px / udm2_total_px) < 0.5
    report_df['udm2_clear_px_to_total_px_ratio'] = \
        report_df['Clear Pixel Count (PSScene4Band-udm2-band_1_count)'] \
        / report_df['Total Pixel Count (PSScene4Band-udm2-total_px_count)']

    report_df['Detection Best Guess With UDM1 and UDM2'] = \
                        (report_df['Total Object Count'] \
                        / (report_df['udm2_clear_px_to_total_px_ratio'] \
                        * report_df['Total Pixel Count (PSScene3Band-udm-total_px_count)'])) \
                        * report_df['Total Pixel Count (PSScene4Band-udm2-total_px_count)'].mean()
         
    return report_df.query('udm2_clear_px_to_total_px_ratio > 0.5')
    

def get_report_data_from_widget_selection(subscription_widget, indexed_stats_df, pl_api_key):
    description = subscription_widget
    selection = indexed_stats_df.query('Description == @description')

    subscription_id = selection['Subscription ID'].iloc[0]
    report_url = selection['Stats Report Link'].iloc[0]
    sif_env_name = selection['SIF Env'].iloc[0]
    object_class = selection['Object type/class'].iloc[0]

    if sif_env_name == 'Live':
        sif_env = 'sif-live'
    else:
        sif_env = 'sif-next'
        
    print(report_url)
    report_data = get_report_data(report_url, pl_api_key)
    report_df = restructure_results(report_data)
    
    if object_class in ['Ships', 'Airplanes']:
        report_df = cloud_normalize_results_df(report_df)
    
    return report_df

def vizualize_report_data_from_widget_selection(subscription_widget, indexed_stats_df, pl_api_key):
    description = subscription_widget
    selection = indexed_stats_df.query('Description == @description')
    object_class = selection['Object type/class'].iloc[0]

    report_df = get_report_data_from_widget_selection(subscription_widget, indexed_stats_df, pl_api_key)
    
    if object_class in ['Ships', 'Airplanes', 'Wellpads']:
        timeseries_viz = report_df[
            [
                'Total Object Count',
                'Detections by Number of Clear Pixels',
                'Detection Best Guess With UDM1 and UDM2'
            ]
        ].hvplot().options(xformatter=xformatter, width=1000)
    else:
        timeseries_viz = report_df[
            [
                'Feature Pixel Count',
                'Total Pixel Count'
            ]
        ].hvplot().options(xformatter=xformatter, width=1000)
    return report_df, timeseries_viz

def post_stats_report_job_request(subscription_id, 
                                aoi_name, 
                                subscription_class,
                                time_interval,
                                pl_api_key, 
                                start_date = None,
                                end_date = None,
                                sub_aoi_geometry = None,
                                sif_env='sif-live'):
    # Setup Basic Auth
    BASIC_AUTH = (pl_api_key, '')
    session = requests.Session()
    session.auth=BASIC_AUTH
    
    title = f"{aoi_name} Cloud Contextualized {subscription_class} Statistics: Subscription {subscription_id}"
    if start_date:
        title += " {start_date} -"
    if end_date:
        title += " {end_date}"
    print(title)
    
    request_body = {
        "title": title,
        "subscriptionID": subscription_id,
        "interval": time_interval
    }
    
    if start_date:
        request_body = request_body.update({"startTime": start_date})
    if end_date:
        request_body = request_body.update({"endTime": end_date})
    if sub_aoi_geometry:
        request_body = request_body.update({"collection": sub_aoi_geometry})
        
    
    SIF_BASE_URL = f'https://{sif_env}.prod.planet-labs.com/'
    stats_post_url = SIF_BASE_URL + 'stats'

    job_post_resp = requests.post(
        stats_post_url, 
        data=json.dumps(request_body), 
        auth=BASIC_AUTH,
        headers={'content-type':'application/json'}
    )

    job_link = job_post_resp.json()['links'][0]['href']
    status = "pending"
    while status not in ["completed", "failed"]:
        report_status_resp = requests.get(
            job_link,
            auth=BASIC_AUTH,
        )
        status = report_status_resp.json()['status']
        print(status)
        time.sleep(2)
    
    report_results_link = report_status_resp.json()['links'][-1]['href']
    
    results_resp = requests.get(
        report_results_link,
        auth=BASIC_AUTH,
    )
    
    return results_resp.status_code, results_resp.json()