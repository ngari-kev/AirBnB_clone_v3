#!/usr/bin/python3
"""A module for managing Review objects in the application."""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    """Retrieves a list of all Review objects of a specific Place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = [review.to_dict() for review in storage.all("Review").values()
               if review.place_id == place_id]

    response = make_response(jsonify(reviews))
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieves a specific Review object by its ID."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    response = make_response(jsonify(review.to_dict()))
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a specific Review object by its ID."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    response = make_response(jsonify({}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a new Review object in a specific Place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if 'user_id' not in request_data:
        abort(400, "Missing user_id")
    if 'text' not in request_data:
        abort(400, "Missing text")

    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)

    new_review = Review(text=request_data['text'], place_id=place_id,
                        user_id=request_data['user_id'])
    storage.new(new_review)
    storage.save()

    response = make_response(jsonify(new_review.to_dict()), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates an existing Review object by its ID."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")

    ignore_keys = {'id', 'user_id', 'place_id', 'created_at', 'updated_at'}
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    storage.save()

    response = make_response(jsonify(review.to_dict()), 200)
    response.headers["Content-Type"] = "application/json"
    return response
