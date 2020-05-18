import stats_utils
import pandas as pd
import streamlit as st
import os
import pydeck as pdk 
import json
import geopandas as gpd
import hvplot
import hvplot.pandas
import holoviews as hv 
hv.extension('bokeh')

API_KEY = os.environ['PL_API_KEY']

def display_timeseries_data(subscription_selection, indexed_stats_df, pl_api_key):
    report_df, timeseries_viz = stats_utils.vizualize_report_data_from_widget_selection(subscription_selection, indexed_stats_df, pl_api_key)
    st.bokeh_chart(hv.render(timeseries_viz, backend='bokeh'))
    st.dataframe(report_df)

def make_subscription_map(subscription_selection):
    subscription_geometry = stats_utils.get_stats_geometry_from_widget_selection(subscription_selection, indexed_stats_df, API_KEY)

    subscription_gdf = gpd.GeoDataFrame.from_file(json.dumps(subscription_geometry))

    subscription_map = subscription_gdf.hvplot(geo=True)

    st.bokeh_chart(hv.render(subscription_map, backend='bokeh'))

# Load stats indexed subscriptions
indexed_stats_df = pd.read_csv('indexed_stats.csv')
indexed_stats_df = indexed_stats_df.dropna(subset=['Stats Report Link'])
indexed_stats_df = indexed_stats_df[indexed_stats_df['SIF Env'] == 'Live']
subscription_options = indexed_stats_df['Description'].values

subscription_selection = st.selectbox("Pick a Subscription", subscription_options)

make_subscription_map(subscription_selection)

display_timeseries_data(subscription_selection, indexed_stats_df, API_KEY)