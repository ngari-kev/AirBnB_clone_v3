#!/usr/bin/python3
"""A module that renders amenity related objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieves a list of all User objects."""
    users = [user.to_dict() for user in storage.all("User").values()]

    response = make_response(jsonify(users))
    return response


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a specific User object by its ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    response = make_response(jsonify(user.to_dict()))
    return response


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a specific User object by its ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    response = make_response(jsonify({}), 200)
    return response


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a new User object."""
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if 'email' not in request_data:
        abort(400, "Missing email")
    if 'password' not in request_data:
        abort(400, "Missing password")

    new_user = User(email=request_data['email'],
                    password=request_data['password'])
    storage.new(new_user)
    storage.save()

    response = make_response(jsonify(new_user.to_dict()), 201)

    return response


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates an existing User object by its ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")

    ignore_keys = {'id', 'email', 'created_at', 'updated_at'}
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    storage.save()

    response = make_response(jsonify(user.to_dict()), 200)
    return response
