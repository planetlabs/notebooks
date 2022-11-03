import asyncio
import argparse
import json
import logging
import os
from pathlib import Path

LOGGER = logging.getLogger(__name__)


import numpy as np
import planet
from planet import data_filter
import rasterio
import rio_tiler
from shapely.geometry import shape

ITEM_TYPE = "PSScene"
ASSET_TYPE = 'ortho_analytic_4b_sr'

# minimum portion of the AOI that is overlapped by the image footprint
MIN_OVERLAP_PERCENT = 99

def _get_search_filter(aoi_geometry, asset_type=ASSET_TYPE, year=2017):
    return data_filter.and_filter([
        data_filter.permission_filter(),
        data_filter.std_quality_filter(),
        data_filter.range_filter('cloud_cover', lte=0.2),
        data_filter.geometry_filter(aoi_geometry),
        data_filter.asset_filter([asset_type])
        ])


async def get_count(aoi_geometry):
    async with planet.Session() as sess:
        cl = planet.DataClient(sess)
        search_filter = _get_search_filter(aoi_geometry)
        stats = await cl.get_stats([ITEM_TYPE], search_filter=search_filter, interval='year')
        count = sum([b['count'] for b in stats['buckets']])
        print(f'{count} images match search')


async def process(aoi_geometry, asset_type=ASSET_TYPE, limit=2, start=0, save=False, callback=None):
    async with planet.Session() as sess:
        cl = planet.DataClient(sess)
        search_filter = _get_search_filter(aoi_geometry)

        items = await cl.search([ITEM_TYPE], search_filter, limit=limit)

        # make sure the image covers enough of the AOI 
        items = [item async for item in _filter_by_overlaps(items, aoi_geometry)]

        await asyncio.gather(*(process_item(i, asset_type, aoi_geometry, cl, save=save, callback=callback) for i in items))


async def _filter_by_overlaps(items, aoi_geometry):
    aoi_shape = shape(aoi_geometry)
    
    def get_overlap(item):
        item_shape = shape(item['geometry'])
        overlap = 100.0*(aoi_shape.intersection(item_shape).area / aoi_shape.area)
        return overlap
    
    async for item in items:
        if get_overlap(item) > MIN_OVERLAP_PERCENT:
            yield item


async def process_item(item, asset_type, aoi_geometry, cl, save=False, callback=None, stagger=True):
            # activate asset
            item_type = item['properties']['item_type']
            item_id = item['id']
            
            print(f'{item_id}: activating')
            asset = await cl.get_asset(item_id=item_id, asset_type_id=asset_type, item_type_id=item_type)
            await cl.activate_asset(asset)
            print(f'{item_id}: waiting')
            asset = await cl.wait_asset(asset)
            
            location = asset['location']
            out_filename = f'{item_id}.tif' if save else None

            print(f'{item_id}: processing')
            stats = await process_asset(location, aoi_geometry, out_filename=out_filename, do_show=False)
            stats['item_id'] = item_id
            stats['date'] = item['properties']['acquired']

            if callback:
                callback(stats)
            return stats


async def process_asset(location, aoi_geometry, out_filename=None, do_show=False):
            # vsicurl driver enables accessing as a cog
            vsi_url = f'/vsicurl/{location}' 

            with rio_tiler.io.COGReader(vsi_url) as cog:
                data = cog.feature(aoi_geometry).as_masked()
          
                if do_show:
                    rasterio.plot.show((data.astype(np.float64) / 2**4).astype(np.uint8))

                if out_filename:
                    profile = cog.dataset.profile
                    with rasterio.open(out_filename, 'w', **profile) as dst:
                        dst.write(data)

                ndvi = (data[3] - data[2]) / (data[3] + data[2])
                data = np.ma.concatenate((data, ndvi[np.newaxis, ...]), axis=0)
                LOGGER.info(data.shape)
                stats = {
                    'mean': list(np.ma.mean(data, axis=(1, 2))),
                    'std': list(np.ma.std(data, axis=(1, 2))),
                    'median': list(np.ma.median(data, axis=(1, 2))),
                    'count': list(np.ma.count(data, axis=(1, 2)).astype(float)),
                }
            return stats

class Manager():
    def __init__(self, field_geojson):
        self.id = field_geojson['id']
        self.stats = []
    
    def accumulate(self, stats):
        item_stats = stats.copy()
        item_stats['id'] = self.id
        self.stats.append(stats)
        # print(len(self.stats))
        
    def save(self):
        root = Path('data', 'run2', 'results')
        root.mkdir(parents=True, exist_ok=True)
        path = root / f'{self.id}.json'
        with open(path, "w") as f:
            f.write(json.dumps(self.stats))

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


async def main(field_geojson, limit=5):
    mgr = Manager(field_geojson)
    try:
        # the stats get accumulated by mgr.accumulate which is called for each cog overlapping field_geojson
        await process(field_geojson['geometry'], limit=limit, save=False, callback=mgr.accumulate)
    finally:
        print('saving results')
        mgr.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get stats for cogs that overlap field described as geojson.')
    parser.add_argument('filename')
    parser.add_argument('--count', action='store_true')
    parser.add_argument('--limit', type=int, default=1)

    args = parser.parse_args()
    field_geojson = load_json(args.filename)

    if args.count:
        asyncio.run(get_count(field_geojson['geometry']))
    else:
        asyncio.run(main(field_geojson, args.limit))
