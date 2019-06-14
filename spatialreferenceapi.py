#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
spatialreferenceapi.py -- A lightweight API for spatialreference.org

Author:
Garin Wally; June 14, 2019

License:
MIT (see README.md)
"""

import json
import re
import requests


# URL to Spatial Reference System (srs) string
_site = "https://spatialreference.org/ref/{auth}/{srid}/{fmt}/"

# Supported Authorities
_authorities = ["epsg", "esri", "sr-org"]

# Supported Formats
_formats = [
    'html',
    'prettywkt',
    'proj4',
    'json',
    'gml',
    'esriwkt',
    'mapfile',
    'mapserverpython',
    'mapnik',
    'mapnikpython',
    'geoserver',
    'postgis',
    'spatialite',  # Customized in the get function: derrivitive of PostGIS
    'proj4js'
    ]


class SpatialReferenceResponse(object):
    """Response object returned by spatialreferenceapi.get()."""
    def __init__(self, auth, srid, sr_format, text):
        self.auth = auth
        self.srid = srid
        self.sr_format = sr_format
        self.text = text
        self.url = _site.format(auth=auth, srid=srid, fmt=sr_format)

    def to_json(self):
        """Returns the object as a json string."""
        return json.dumps(self.__dict__)

    def __getitem__(self, key):
        # Allow the object to be treated as a dictionary supporting:
        #  sr["srid"] == 102700
        return getattr(self, key)

    def __str__(self):
        return self.to_json()


def get(srid, auth, sr_format, raise_errors=True):
    """RESTful GET function for spatialreference.org.
    Args:
        srid (int/str): Spatial Reference ID
        auth (str): Spatial Reference Authority
        sr_format (str): the requested format of the spatial reference info
        raise_errors (bool): Turn raising errors on/off (default: True)
    Returns a SpatialReferenceResponse object with the requested format of the
    spatial reference system.
    """
    site = "https://spatialreference.org/ref/{0}/{1}/{2}/"
    # Validate inputs
    srid = int(srid)
    auth = auth.lower()
    sr_format = sr_format.lower()
    if auth not in _authorities:
        raise ValueError("{} is not a valid authority".format(auth))
    if sr_format not in _formats:
        raise ValueError("{} is not a valid format".format(sr_format))

    # SpatiaLite is PostGIS with an alteration
    if sr_format == "spatialite":
        r = requests.get(site.format(auth, srid, "postgis"))
        txt = re.sub("9{}".format(srid), str(srid), r.text, count=1)
    # All other types
    else:
        r = requests.get(site.format(auth, srid, sr_format))
        txt = r.text

    # Raise errors on unsuccessful calls (if raise_errors is True)
    if raise_errors:
        if r.status_code == 404:
            raise requests.HTTPError("404 - Not Found")
        elif r.status_code != 200:
            raise requests.HTTPError("Error: Status Code {}".format(
                r.status_code))

    # Return the response as a customized object
    return SpatialReferenceResponse(auth, srid, sr_format, txt)
