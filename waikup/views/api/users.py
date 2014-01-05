# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from peewee import DoesNotExist

from waikup.lib.errors import ApiError
from waikup.lib.helpers import required_fields
from waikup.views.api import Resource, ResourceSet, login_required

users = Blueprint('users', __name__)


class UserResource(Resource):
    name = 'user'
    fields = ('username', 'first_name', 'last_name', 'email', 'admin', 'active')


class TokenResource(Resource):
    name = 'token'
    fields = ('token', 'user')
    fk_map = {'user': 'username'}


@users.route('/auth', methods=['POST'])
@required_fields('username', 'password')
def auth():
    """Authenticate an user and reply with its auth token."""
    from waikup.models import User
    try:
        user = User.get(User.username == request.form['username'])
        if not user.check_password(request.form['password']):
            raise ApiError("Invalid credentials", status_code=403)
    except ApiError:
        raise ApiError("Invalid credentials", status_code=403)
    token = user.generate_token()
    data = TokenResource(token).data
    return jsonify(data)


@users.route('/deauth', methods=['POST'])
def deauth():
    """Delete given token."""
    from waikup.models import Token
    token_str = request.headers['Auth']
    token = Token.get(Token.token == token_str)
    return jsonify({"success": True})


@users.route('/')
@login_required(admin=True)
def list_users():
    """Get all users in database."""
    from waikup.models import User
    user_objs = list(User.select())
    data = ResourceSet(UserResource, user_objs).data
    return jsonify(data)


@users.route('/<int:userid>')
@login_required(admin=True)
def get_user(userid):
    """Get user with given ID."""
    from waikup.models import User
    try:
        user = User.get(User.id == userid)
        data = UserResource(user).data
    except DoesNotExist:
        raise ApiError("User not found: %d" % userid, status_code=404)
    return jsonify(data)


@users.route('/', methods=['POST'])
@login_required(admin=True)
@required_fields('username', 'first_name', 'last_name', 'email', 'password')
def create_user():
    """Create a new user."""
    from waikup.models import User
    user = User.create(
        username=request.form.get('username'),
        first_name=request.form.get('first_name'),
        last_name=request.form.get('last_name'),
        email=request.form.get('email')
    )
    user.set_password(request.form.get('password'))
    user.save()
    return jsonify({"success": True})


@users.route('/<int:userid>', methods=['PUT'])
@login_required(admin=True)
def update_user(userid):
    """Update informations for user with given ID."""
    # TODO: find a way to allow an user to update its own informations
    from waikup.models import User
    user = User.get(User.id == userid)
    user.safe_update(request.form)
    if 'password' in request.form:
        user.set_password(request.form['password'])
        user.save()
    return jsonify({"success": True})


@users.route('/<int:userid>', methods=['DELETE'])
@login_required(admin=True)
def delete_user(userid):
    """Delete user with given ID."""
    from waikup.models import User
    User.safe_delete(User.id == userid)
    return jsonify({"success": True})