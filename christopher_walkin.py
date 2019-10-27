# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: christopher_walkin.py
"""

import requests

def walk_to_washington_monument(origin, apikey):
    """take an origin string (an address, place id, or lat,lon pair (even
    lat,lon is a string)) and an api key, and return the time it would take to
    *walk* from there. the destination parameter has value
    "The Washington Monument"

    """
    # make the request (destination is "The Washington Monument", mode is walking)
    #---------------#

    request = requests.get(
        url='https://maps.googleapis.com/maps/api/directions/json',
        params={
            'origin': origin,
            'destination': 'The Washington Monument',
            'key': apikey,
            'mode': 'walking'
        }
    )
    #---------------#

    # extract the entire json dictionary from the response object we received
    #---------------#
    r = request.json()
    #---------------#

    # extract the duration from the json response dictionary, in seconds
    #---------------#
    duration = r['routes'][0]['legs'][0]['duration']['value']
    #---------------#

    return duration
