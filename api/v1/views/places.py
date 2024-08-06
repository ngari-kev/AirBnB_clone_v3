#!/usr/bin/python3
"""A module for managing Place objects in the application."""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """Retrieves a list of all Place objects of a specific City."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in storage.all("Place").values()
              if place.city_id == city_id]

    response = make_response(jsonify(places))
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a specific Place object by its ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    response = make_response(jsonify(place.to_dict()))
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a specific Place object by its ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    response = make_response(jsonify({}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a new Place object in a specific City."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if 'user_id' not in request_data:
        abort(400, "Missing user_id")
    if 'name' not in request_data:
        abort(400, "Missing name")

    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)

    new_place = Place(name=request_data['name'], city_id=city_id,
                      user_id=request_data['user_id'])
    storage.new(new_place)
    storage.save()

    response = make_response(jsonify(new_place.to_dict()), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates an existing Place object by its ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")

    ignore_keys = {'id', 'user_id', 'city_id', 'created_at', 'updated_at'}
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()

    response = make_response(jsonify(place.to_dict()), 200)
    response.headers["Content-Type"] = "application/json"
    return response
