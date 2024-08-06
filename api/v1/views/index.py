#!/usr/bin/python3
"""Index Route"""

from models import storage
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """Returns status OK"""
    return jsonify({'status': 'OK'})
