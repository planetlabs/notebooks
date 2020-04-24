from _ctypes import PyObj_FromPtr
from copy import deepcopy
import json
import re
import numbers

import geojson
from geojson import Polygon, Feature, FeatureCollection


# https://stackoverflow.com/questions/13249415/how-to-implement-custom-indentation-when-pretty-printing-with-the-json-module
class NoIndentCoordinate(object):
    """ Value wrapper. """
    def __init__(self, value):
        self.value = value


class CoordinateEncoder(geojson.GeoJSONEncoder):
    FORMAT_SPEC = '@@{}@@'
    regex = re.compile(FORMAT_SPEC.format(r'(\d+)'))

    def __init__(self, **kwargs):
        # Save copy of any keyword argument values needed for use here.
        self.__sort_keys = kwargs.get('sort_keys', None)
        super(CoordinateEncoder, self).__init__(**kwargs)

    def default(self, obj):
        val = (self.FORMAT_SPEC.format(id(obj))
               if isinstance(obj, NoIndentCoordinate)
               else super(CoordinateEncoder, self).default(obj))
        return val

    def encode(self, obj):
        format_spec = self.FORMAT_SPEC  # Local var to expedite access.
        json_repr = super(CoordinateEncoder, self).encode(obj)  # Default JSON.

        # Replace any marked-up object ids in the JSON repr with the
        # value returned from the json.dumps() of the corresponding
        # wrapped Python object.
        for match in self.regex.finditer(json_repr):
            # see https://stackoverflow.com/a/15012814/355230
            id = int(match.group(1))
            no_indent = PyObj_FromPtr(id)
            json_obj_repr = json.dumps(no_indent.value, sort_keys=self.__sort_keys)

            # Replace the matched id string with json formatted representation
            # of the corresponding Python object.
            json_repr = json_repr.replace(
                            '"{}"'.format(format_spec.format(id)), json_obj_repr)

        return json_repr


class CompactFeature(Feature):
    def __repr__(self):
        return geojson.dumps(self.specify_coords(), cls=CoordinateEncoder, indent=4)
    
    __str__ = __repr__
    
    def specify_coords(self):
        def is_coords(c):
            '''Answering: is this object a set of 2D coordinates?'''
            if len(c) != 2:
                return False
            for v in c:
                if not isinstance(v, numbers.Number):
                    return False
            return True

        def noindent_coords(coords):
            '''Find the coordinates and  '''
            if is_coords(coords):
                return NoIndentCoordinate(coords)
            else:
                for i, c in enumerate(coords):
                    coords[i] = noindent_coords(c)
                return coords

        try:
            p = deepcopy(self)
            p['geometry']['coordinates'] = noindent_coords(p['geometry']['coordinates'])
        except (KeyError, TypeError):
            pass
        return p


class CompactFeatureCollection(FeatureCollection):
    def __init__(self, **extras):
        super(FeatureCollection, self).__init__(**extras)
        self.type = 'FeatureCollection'

    def __repr__(self):
        return geojson.dumps(self.specify_coords(), cls=CoordinateEncoder, indent=4)
    
    __str__ = __repr__
    
    def specify_coords(self):
        try:
            p = deepcopy(self)
            p.features = [f.specify_coords() for f in p.features]
        except (KeyError, TypeError):
            pass
        return p        
