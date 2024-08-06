#!/usr/bin/python3
"""Index Route"""

from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns status OK"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """Returns a all classes and number of instances for each"""
    classes = {
        'states': "State",
        'users': "User",
        'amenities': "Amenity",
        'cities': "City",
        'places': "Place",
        'reviews': "Review"
    }
    counts = {}

    
    for k, v in classes.items():
        count = storage.count(v)
        print("counting {}: {}".format(v, count))
        counts[k] = count
    counts = dict(sorted(counts.items()))
    return jsonify(counts)
