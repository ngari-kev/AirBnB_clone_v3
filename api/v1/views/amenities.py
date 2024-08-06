#!/usr/bin/python3
"""A module that renders amenity related objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities')
def list_amenities():
    """Retrieves a list of all amenity objects."""
    amenity_list = [amenity.to_dict() for amenity in
                    storage.all("Amenity").values()]

    response = make_response(jsonify(amenity_list))
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/amenities/<amenity_id>')
def retrieve_amenity(amenity_id):
    """Retrieves a specific amenity object by its ID."""
    amenities = storage.all("Amenity").values()
    amenity_data = [amenity.to_dict() for amenity in amenities
                    if amenity.id == amenity_id]

    if not amenity_data:
        abort(404)
    response = make_response(jsonify(amenity_data[0]))
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def remove_amenity(amenity_id):
    """Deletes a specific amenity object by its ID."""
    amenity_instance = storage.get(Amenity, amenity_id)

    if not amenity_instance:
        abort(404)

    storage.delete(amenity_instance)
    storage.save()

    response = make_response(jsonify({}), 200)
    return response


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates a new amenity object."""

    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")

    if 'name' not in request_data:
        abort(400, "Missing name")

    new_amenity = Amenity(name=request_data['name'])
    storage.new(new_amenity)
    storage.save()

    amenity_info = new_amenity.to_dict()
    response = make_response(jsonify(amenity_info), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def modify_amenity(amenity_id):
    """Updates an existing amenity object by its ID."""
    amenities = storage.all("Amenity").values()
    amenity_data = [amenity.to_dict() for amenity in amenities
                    if amenity.id == amenity_id]

    if not amenity_data:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")

    for amenity in amenities:
        if amenity.id == amenity_id:
            amenity.name = request_data['name']

    storage.save()

    response = make_response(jsonify(amenity_data[0]), 200)
    return response
