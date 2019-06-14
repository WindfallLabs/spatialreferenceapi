# spatialreferenceapi.py:
A lightweight API for [spatialreference.org](https://spatialreference.org/)

## About:
This small module provides a RESTful GET function to retrieve spatial reference system
strings from spatialreference.org (using the requests library) and return them as
a dictionary-like `SpatialReferenceResponse` object (which easily converts
to a json string with the `.to_json()` method).  

The goal of this project is to get spatial reference system strings in various
formats by authority and Spatial Reference ID (srid). We hope that this
project provides a simplistic alternative to `osgeo.osr.SpatialReference`
objects, and allows users access to spatial reference systems that might not have
access to larger geographic data libraries (e.g. GDAL, osgeo, etc.)
 
## License:
```
MIT License

Copyright (c) 2019 Garin Wally

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Credits:
This project would not be possible without the hard work from the awesome folks behind
[spatialreference.org](https://spatialreference.org/about/).

## Examples (doctests):
(Execute tests with `$ python -m doctest -v README.md`)  

    >>> import spatialreferenceapi as srapi

    # Request a unicode srs string from spatialreference.org
    >>> sr = srapi.get(102700, "esri", "postgis")

    # The text property contains the desired srs unicode string
    >>> sr.text.startswith("INSERT") and len(sr.text) > 50
    True

    # Data can be accessed via properties or using dict-keys
    >>> sr.srid == 102700 and sr["srid"] == 102700
    True

    >>> sr.auth == "esri" and sr["auth"] == "esri"
    True

    # Easily converts from object to json string
    >>> sr.to_json().startswith("{") and sr.to_json().endswith("}")
    True

    # The object's string representation (__str__) is an alias for '.to_json'
    >>> sr.to_json() == str(sr)
    True

    # GET Requests raise errors when incorrect authorities are used
    #  i.e. the URL does not exist and results in a 404 error
    #  (Note that 102700 is an 'esri' authority spatial reference id)
    >>> sr = srapi.get(102700, "epsg", "postgis")
    Traceback (most recent call last):
    HTTPError: 404 - Not Found

    # Raising errors can be turned off
    >>> sr = srapi.get(102700, "epsg", "postgis", raise_errors=False)

    >>> sr.text.startswith(u'Not found,')
    True

    # Note that SpatiaLite is not hosted on spatialreference.org it is derrived
    #  from the 'postgis' format (which adds a leading '9' to the srid).
    >>> sr = srapi.get(102700, "esri", "spatialite")

    >>> import re

    >>> re.findall(" \d+", sr.text)[0] != " 9102700"
    True


## Contributing:
Contributions are welcome, but I think this project is functionally complete.
I welcome additional formats which can be converted from those hosted on
[spatialreference.org](https://spatialreference.org/) (such as the conversion from PostGIS to SpatiaLite I've included).
I'm not interested in PUT/POST functionality; adding customized spatial reference systems to the site should be done manually.
