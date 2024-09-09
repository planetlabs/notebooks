"""
A standalone client for the Planet Basemaps API.
"""
import os
import re
import json
import shutil
import datetime as dt
import itertools as it
from concurrent.futures import ThreadPoolExecutor

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# GDAL XYZ XML templates for full-bit-depth streaming.
FULL_BIT_DEPTH_XML = """
<GDAL_WMS>
        <Service name="TMS">
        <ServerUrl>{tileserver}?api_key={api_key}{extra}&amp;format=geotiff&amp;proc=off</ServerUrl>
        </Service>
        <DataWindow>
            <UpperLeftX>-20037508.34</UpperLeftX>
            <UpperLeftY>20037508.34</UpperLeftY>
            <LowerRightX>20037508.34</LowerRightX>
            <LowerRightY>-20037508.34</LowerRightY>
            <TileLevel>{level}</TileLevel>
            <TileCountX>1</TileCountX>
            <TileCountY>1</TileCountY>
            <YOrigin>top</YOrigin>
        </DataWindow>
        <Projection>EPSG:3857</Projection>
        <BlockSizeX>256</BlockSizeX>
        <BlockSizeY>256</BlockSizeY>
        <BandsCount>{nbands}</BandsCount>
        <ZeroBlockHttpCodes>404</ZeroBlockHttpCodes>
        <ZeroBlockOnServerException>true</ZeroBlockOnServerException>
        <DataValues NoData="{nodata}" min="{mins}" max="{maxs}" />
        <DataType>{datatype}</DataType>
        <Cache/>
</GDAL_WMS>
""".lstrip()


FULL_BIT_DEPTH_PROC_XML = """
<GDAL_WMS>
        <Service name="TMS">
        <ServerUrl>{tileserver}?api_key={api_key}{extra}&amp;format=geotiff&amp;proc={proc}</ServerUrl>
        </Service>
        <DataWindow>
                <UpperLeftX>-20037508.34</UpperLeftX>
                <UpperLeftY>20037508.34</UpperLeftY>
                <LowerRightX>20037508.34</LowerRightX>
                <LowerRightY>-20037508.34</LowerRightY>
                <TileLevel>{level}</TileLevel>
                <TileCountX>1</TileCountX>
                <TileCountY>1</TileCountY>
                <YOrigin>top</YOrigin>
        </DataWindow>
        <Projection>EPSG:3857</Projection>
        <BlockSizeX>256</BlockSizeX>
        <BlockSizeY>256</BlockSizeY>
        <BandsCount>1</BandsCount>
        <ZeroBlockHttpCodes>404</ZeroBlockHttpCodes>
        <ZeroBlockOnServerException>true</ZeroBlockOnServerException>
        <DataValues min="-1" max="1" />
        <DataType>Float32</DataType>
        <Cache/>
</GDAL_WMS>
""".lstrip()


def _get_client(client):
    if client is None:
        client = BasemapsClient()

    if not client.api_key:
        raise ValueError(
            'No API key provided! Either set the PL_API_KEY environment '
            'variable or use the api_key parameter'
        )

    return client


def _chunks(iterable, chunksize):
    iterable = iter(iterable)
    while True:
        v = tuple(it.islice(iterable, chunksize))
        if v:
            yield v
        else:
            return


class BasemapsClient(object):
    """Demo client for working with the Planet basemaps API"""

    base_url = 'https://api.planet.com/basemaps/v1'

    def __init__(self, api_key=None):
        """
        :param str api_key:
            Your Planet API key. If not specified, this will be read from the
            PL_API_KEY environment variable.
        """
        if api_key is None:
            api_key = os.getenv('PL_API_KEY')
        self.api_key = api_key

        self.session = requests.Session()
        self.session.auth = (api_key, '')

        retries = Retry(total=5, backoff_factor=0.2, status_forcelist=[429])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def _url(self, endpoint):
        return '{}/{}'.format(self.base_url, endpoint)

    def _consume_pages(self, endpoint, key, **params):
        """General pagination structure for Planet APIs."""
        url = self._url(endpoint)
        while True:
            response = self._get(url, **params)
            for item in response[key]:
                yield item

            if '_next' in response['_links']:
                url = response['_links']['_next']
            else:
                break

    def _query(self, endpoint, key, json_query):
        """Post and then get for pagination. Being lazy here and repeating."""
        url = None

        while True:
            if url is None:
                url = self._url(endpoint)
                response = self._post(url, json_query)
            else:
                response = self._get(url)

            for item in response[key]:
                yield item

            if '_next' in response['_links']:
                url = response['_links']['_next']
            else:
                break

    def _list(self, endpoint, key=None, **params):
        key = key or endpoint
        for item in self._consume_pages(endpoint, key, **params):
            yield item

    def _get(self, url, **params):
        rv = self.session.get(url, params=params)
        rv.raise_for_status()
        return rv.json()

    def _post(self, url, json_data):
        rv = self.session.post(url, json=json_data)
        rv.raise_for_status()
        return rv.json()

    def _item(self, endpoint, **params):
        return self._get(self._url(endpoint), **params)

    def _download(self, url, filename=None, output_dir=None):
        response = self.session.get(url, stream=True)
        response.raise_for_status()

        disposition = response.headers['Content-Disposition']
        if filename is None:
            filename = re.findall(r'filename="(.+)"', disposition)[0]

        if filename is None:
            msg = 'Filename not specified and no content-disposition info!'
            raise ValueError(msg)

        if output_dir is not None:
            try:
                os.mkdir(output_dir)
            except OSError:
                # Due to threading, the directory may be created simultaneously
                pass
            filename = os.path.join(output_dir, filename)

        # Download in chunks.
        with open(filename, 'wb') as outfile:
            shutil.copyfileobj(response.raw, outfile)
        del response

        return filename

    def series(self, name=None, series_id=None):
        """
        Retrieve a MosaicSeries object for a specific series by either name or
        ID. You must specify either name or series_id, but not both.

        :param str name:
            The name of the series (e.g. "Global Monthly")
        :param str series_id:
            The series ID (e.g. "431b62a0-eaf9-45e7-acf1-d58278176d52")

        :returns MosaicSeries:
            An object representing the series
        """
        if name is not None:
            return MosaicSeries.from_name(name, self)
        elif series_id is not None:
            return MosaicSeries.from_id(series_id, self)
        else:
            raise ValueError('You must specify either name or series_id!')

    def list_series(self, name_contains=None):
        """
        Iterate through all mosaic series you have access to, optionally
        filtering based on name. Yields ``MosaicSeries`` instances.

        :param str name_contains:
            Search only for series that contain the specified substring in
            their names
        """
        for item in self._list('series', name__contains=name_contains):
            yield MosaicSeries(item, self)

    def list_mosaics(self, name_contains=None):
        """
        Iterate through all mosaics you have access to, optionally filtering
        based on name. Yields ``Mosaic`` instances.

        :param str name_contains:
            Search only for mosaics that contain the specified substring in
            their names
        """
        for item in self._list('mosaics', name__contains=name_contains):
            yield Mosaic(item, self)

    def mosaic(self, name=None, mosaic_id=None):
        """
        Retrieve a `Mosaic` object for a particular mosaic, either by name or
        ID. You must specify either name or mosaic_id, but not both.

        :param str name:
            The name of the mosaic (e.g. "global_monthly_2019_09_mosaic")
        :param str mosaic_id:
            The mosaic ID (e.g. "431b62a0-eaf9-45e7-acf1-d58278176d52")

        :returns Mosaic:
            An object representing the mosaic
        """
        if name is not None:
            return Mosaic.from_name(name, self)
        elif mosaic_id is not None:
            return Mosaic.from_id(mosaic_id, self)
        else:
            raise ValueError('You must specify either name or mosaic_id!')


class MosaicSeries(object):
    """Represents a collection of mosaics, usually on a regular interval."""

    def __init__(self, info, client=None):
        """
        :param dict info:
            The JSON api response for the series from the mosaic api
        :param BasemapsClient client:
            A specific Client instance to use. Will be created if not specified.
        """
        self.client = _get_client(client)

        self.id = info['id']
        self.name = info['name']
        self.info = info
        self.links = self.info.pop('_links', {})

    @classmethod
    def from_name(cls, name, client=None):
        """
        Initialize a series based on its exact name.
        """
        client = _get_client(client)
        results = list(client._list('series', name__is=name))
        if not results:
            raise ValueError(f'Series {name} not found!')
        return cls(results[0], client)

    @classmethod
    def from_id(cls, series_id, client=None):
        """
        Initialize a series based on its ID.
        """
        client = _get_client(client)
        info = client._item(f'series/{self.id}')
        return cls(info, client)

    def mosaics(self, start_date=None, end_date=None):
        """
        Iterate through mosaics in this series, optionally between the specified
        start and end dates.

        :param str,datetime start_date:
            The earliest date to use. Note that this check is based on the
            first_acquired metadata for the mosaic.
        :param str,datetime end:
            The earliest date to use. Note that this check is based on the
            last_acquired metadata for the mosaic.
        """
        params = {}
        if start_date is not None:
            params['acquired__gt'] = str(start_date)
        if end_date is not None:
            params['acquired__lt'] = str(end_date)

        endpoint = 'series/{}/mosaics'.format(self.id)
        for info in self.client._list(endpoint, key='mosaics', **params):
            mosaic = Mosaic(info, self.client)
            yield mosaic

    def download_quads(self, region=None, bbox=None, start_date=None,
                       end_date=None, nthreads=16, flat=False,
                       filename_template=None):
        """
        Download quads for all mosaics in the series. Will be downloaded into
        separate folders based on mosaic names.

        :param dict region:
            A GeoJSON polygon region
        :param tuple bbox:
            A min_lon, min_lat, max_lon, max_lat tuple.
        :param datetime start_date:
            The earliest date to use. Note that this check is based on the
            first_acquired metadata for the mosaic.
        :param datetime end_date:
            The earliest date to use. Note that this check is based on the
            last_acquired metadata for the mosaic.
        :param int nthreads:
            Number of concurrent downloads.
        :param bool flat:
            By default, quads will be placed in separate, newly-created
            folders.  This option places all quads in the specified folder with
            the mosaic name included in the filename.
        :param str filename_template:
            A {} style format string with the keys "mosaic", "level", "x", "y".
            Defaults to the Content-Deposition sepecified by the API. (i.e.
            typically "L{z}-{x}E-{y}N.tif")
        """
        if flat and not filename_template:
            filename_template = '{mosaic}-L{level}-{x:04d}E-{y:04d}N.tif'

        def all_quads():
            for mosaic in self.mosaics(start_date, end_date):
                for quad in mosaic.quads(bbox, region):
                    if quad.downloadable:
                        yield quad

        def download(quad):
            filename, output_dir = None, None
            if not flat:
                output_dir = quad.mosaic_name

            if filename_template is not None:
                filename = filename_template.format(mosaic=quad.mosaic_name,
                                                    level=quad.level,
                                                    x=quad.x,
                                                    y=quad.y)
            return quad.download(filename=filename, output_dir=output_dir)

        groups = _chunks(all_quads(), 4 * nthreads)
        with ThreadPoolExecutor(nthreads) as executor:
            for group in groups:
                for path in executor.map(download, group):
                    yield path


class Mosaic(object):
    """Representation of a single mosaic."""

    def __init__(self, info, client=None):
        self.client = _get_client(client)

        self.id = info['id']
        self.name = info['name']
        self.level = info['level']
        self.item_types = info['item_types']
        self.datatype = info['datatype']
        self.info = info
        self.links = self.info.pop('_links', {})

        iso = '%Y-%m-%dT%H:%M:%S.%fZ'
        self.start_date = dt.datetime.strptime(self.info['first_acquired'], iso)
        self.end_date = dt.datetime.strptime(self.info['last_acquired'], iso)

    @classmethod
    def from_name(cls, name, client=None):
        """Look up a mosaic by name in the Planet Basemaps API."""
        client = _get_client(client)
        results = list(client._list('mosaics', name__is=name))
        if not results:
            raise ValueError(f'Mosaic {name} not found!')
        return cls(results[0], client)

    @classmethod
    def from_id(cls, mosaic_id, client=None):
        """Look up a mosaic by ID in the Planet Basemaps API."""
        client = _get_client(client)
        info = client._item(f'mosaics/{mosaic_id}')
        return cls(info, client)

    def _bbox_search(self, bbox):
        if bbox is None:
            bbox = self.info['bbox']

        endpoint = f'mosaics/{self.id}/quads'
        bbox = ','.join(str(item) for item in bbox)
        return self.client._consume_pages(endpoint, 'items', bbox=bbox)

    def _region_search(self, region):
        endpoint = f'mosaics/{self.id}/quads/search'
        return self.client._query(endpoint, 'items', region)

    def quads(self, bbox=None, region=None):
        """
        Retrieve info for all quads within a specific AOI specified as either a
        lon/lat ``bbox`` or a geojson ``region``.

        :param tuple bbox:
            A 4-item tuple of floats.  Expected to be (longitude_min,
            latitude_min, longitude_max, latitude_max).
        :param dict region:
            A GeoJSON geometry (usually polygon or multipolygon, not a feature
            collection) in WGS84 representing the exact AOI.
        """
        if region:
            quads = self._region_search(region)
        else:
            quads = self._bbox_search(bbox)

        for info in quads:
            yield MosaicQuad(info, self, self.client)

    def download_quads(self, output_dir=None, bbox=None, region=None,
                       nthreads=16, filename_template=None):
        """
        Download mosaic data to a local directory for a specific AOI specified
        as either a lon/lat ``bbox`` or a geojson ``region``.

        :param tuple bbox:
            A 4-item tuple of floats.  Expected to be (longitude_min,
            latitude_min, longitude_max, latitude_max).
        :param dict region:
            A GeoJSON geometry (usually polygon or multipolygon, not a feature
            collection) in WGS84 representing the exact AOI.
        :param int nthreads:
            Number of concurrent downloads.
        :param str filename_template:
            A {} style format string with the keys "mosaic", "level", "x", "y".
            Defaults to the Content-Deposition sepecified by the API. (i.e.
            typically "L{z}-{x}E-{y}N.tif")
        """

        def download(quad):
            if filename_template is not None:
                filename = filename_template.format(mosaic=self.name,
                                                    level=quad.level,
                                                    x=quad.x,
                                                    y=quad.y)
            else:
                filename = None

            quad.download(filename=filename, output_dir=output_dir)

        quads = self.quads(bbox, region)
        groups = _chunks(quads, 4 * nthreads)
        with ThreadPoolExecutor(nthreads) as executor:
            for group in groups:
                for path in executor.map(download, group):
                    yield path

    @property
    def nbands(self):
        """
        Inferred number of bands (including alpha!) in the mosaic data. May be
        incorrect due to API limitations.
        """
        # This will often be incorrect due to a deficiency in the API. Instead
        # of using metadata, we have to guess based on datatype, and it _will_
        # be wrong some of the time.
        if self.datatype == 'byte':
            # Assume RGB + alpha. Incorrect in many cases.
            return 4
        elif '_8b_' in self.name:
            # Dangerous name-based heuristics, but usually reliable.
            return 9
        else:
            # Sometimes incorrect, but assume it's BGRN + alpha otherwise
            return 5

    def tileserver_xml(self, proc=None, level=None, band_count=None):
        """
        An XML description of the full bit depth streamed data that can be
        opened by gdal/etc.

        :param str proc:
            Processing to apply (e.g. NDVI, etc)
        :param int level:
            Base level to use. Defaults to the base zoom level of the mosaic.
            It is sometimes useful to deliberately use downsampled data for
            regional analysis, in which case you may want a lower zoom level.
        :param int band_count:
            Override guessed band count. Note that the API does not include
            information on band count currently, so this parameter is needed
            when working with 8-band or similar basemaps.

        :retruns str xml:
            XML formatted description. Note that this is directly openable by
            rasterio and gdal without being written to a file.
        """
        extra = '&amp;empty=404'
        maxs, mins, nodata = None, None, None

        if level is None:
            level = self.level

        if band_count is None:
            band_count = self.nbands

        base = 'https://tiles.planet.com/basemaps/v1'
        url = f'{base}/planet-tiles/{self.name}/gmap/${{z}}/${{x}}/${{y}}.tif'

        if proc:
            template = FULL_BIT_DEPTH_PROC_XML

        else:
            template = FULL_BIT_DEPTH_XML

            # Again, assuming SR data, which is possibly not correct
            max_val = "255" if self.datatype == "byte" else "10000"
            max_alpha = "255" if self.datatype == "byte" else "65535"
            maxs = ' '.join((band_count - 1) * [max_val] + [max_alpha])
            mins = ' '.join(band_count * ['0'])

            # Not really, but can't represent an alpha band in this xml format
            nodata = ' '.join(band_count * ['0'])

        return template.format(
                api_key=self.client.api_key,
                datatype=self.datatype,
                extra=extra,
                level=level,
                maxs=maxs,
                mins=mins,
                nbands=band_count,
                nodata=nodata,
                proc=proc,
                tileserver=url,
        )


class MosaicQuad(object):
    """A representation of a single quad."""

    def __init__(self, info, mosaic=None, client=None):
        self.client = _get_client(client)
        self.info = info
        self.links = self.info.pop('_links', {})
        self.id = info['id']
        self.coverage = self.info.get('percent_covered')
        self.bounds = self.info.get('bbox')

        if mosaic is None:
            # Bit odd that quads don't include a mosaic ID directly...
            mosaic_id = self.links['_self'].split('/')[-3]
            mosaic = Mosaic.from_id(mosaic_id)

        self.mosaic = mosaic
        self.mosaic_name = mosaic.name

        x, y = self.id.split('-')
        self.x = int(x)
        self.y = int(y)
        self.level = self.mosaic.level

    @property
    def downloadable(self):
        """Whether or not you have download permissions for the quad."""
        return 'download' in self.links

    @property
    def download_url(self):
        """URL to download or stream COG data."""
        return self.links.get('download')

    def download(self, filename=None, output_dir=None):
        """Download quad data locally."""
        if self.download_url:
            return self.client._download(self.download_url, filename, output_dir)

    def contribution(self):
        """
        Planet data api URLs for each scene that contributed to this quad.
        """
        url = self.links.get('items')
        if url:
            data = self.client._get(url)
            return [item['link'] for item in data['items']]
        else:
            return []
