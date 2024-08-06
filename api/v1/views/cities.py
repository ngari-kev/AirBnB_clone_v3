#!/usr/bin/python3
"""A module for viewing City objects."""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models.city import City
from models import storage

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_in_state(state_id):
    """Retrieves a list of city objects in a state"""
    state = storage.get(State, state_id)
    if not state:
        return make_response(jsonify({'error': 'State not found'}), 404)
    
    cities_list = [obj.to_dict() for obj in storage.all(City).values() if obj.state_id == state_id]
    return make_response(jsonify(cities_list), 200)

@app_views.route('/cities/<city_id>', methods=['GET'])
def a_city(city_id):
    """Retrieves a specific city"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({'error': 'City not found'}), 404)
    
    return make_response(jsonify(city.to_dict()), 200)

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """Deletes a city object wrt id"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({'error': 'City not found'}), 404)
    
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a City object"""
    req_data = request.get_json()
    if not req_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    
    if 'name' not in req_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    
    state = storage.get(State, state_id)
    if not state:
        return make_response(jsonify({'error': 'State not found'}), 404)
    
    new_city = City(name=req_data['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    
    return make_response(jsonify(new_city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({'error': 'City not found'}), 404)
    
    req_data = request.get_json()
    if not req_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    
    for key, value in req_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
