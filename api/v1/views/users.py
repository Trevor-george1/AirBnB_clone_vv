#!/usr/bin/python3
"""User object RESTFul API actions"""

from flask import jsonify, make_response, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """retrieves the list of all user objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)  # noqa
def get_user(user_id):
    """Retrieves a single user by id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users', methods=["POST"], strict_slashes=False)  # noqa
def create_user():
    """creates a User object"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user = User(**data)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)  # noqa
def update_user(user_id):
    """update the user object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)