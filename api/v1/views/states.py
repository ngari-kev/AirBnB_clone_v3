#!/usr/bin/python3
"""A module that renders State objects related methods."""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def statesList():
    """performs a GET function on State for all State objects"""
    allStates = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(allStates)


@app_views.route('/states/<state_id>', methods=['GET'])
def stateID(state_id):
    """performs a GET function on a single State object"""
    allStates = storage.all("State").values()
    state = [obj.to_dict() for obj in allStates if obj.id == state_id]
    if not state:
        abort(404)
    return jsonify(state[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """Performs a DELETE operation on State"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def post():
    """Performs a POST operation on State."""
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    if 'name' not in req_data:
        abort(400, 'Missing name')
    
    new_state = State(name=req_data['name'])
    storage.new(new_state)
    storage.save()
    
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def put(state_id):
    """Perform a PUT operation on State."""
    states = storage.all("State").values()
    
    state_obj = None
    for obj in states:
        if obj.id == state_id:
            state_obj = obj
            break
    
    if not state_obj:
        abort(404, 'State not found')
    
    req_data = request.get_json()
    if not req_data:
        abort(400, 'Not a JSON')
    
    if 'name' in req_data:
        state_obj.name = req_data['name']
    else:
        abort(400, 'Missing name')
    
    storage.save()
    
    return jsonify(state_obj.to_dict()), 200
