# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from peewee import DoesNotExist

from waikup.api import Resource, ResourceSet, login_required, owner_required
from waikup.lib.errors import ApiError
from waikup.lib.helpers import required_fields


links = Blueprint('links', __name__)


class LinkResource(Resource):
    name = 'link'
    fields = ('id', 'url', 'title', 'description', 'submitted', 'author')
    fk_map = {'author': 'username'}


@links.route('/', methods=['GET'])
def list_links():
    """Get all links in database."""
    from waikup.models import Link

    link_objs = list(Link.select())
    data = ResourceSet(LinkResource, link_objs).data
    return jsonify(data)


@links.route('/<int:linkid>', methods=['GET'])
def get_link(linkid):
    """Get link with given ID."""
    from waikup.models import Link
    try:
        link = Link.get(Link.id == linkid)
        data = LinkResource(link).data
    except DoesNotExist:
        raise ApiError("Link not found: %d" % linkid, status_code=404)
    return jsonify(data)


@links.route('/', methods=['POST'])
@login_required()
@required_fields('url', 'title')
def create_link():
    """Create a new link."""
    from waikup.models import Link, User
    token = request.headers['Auth']
    user = User.from_token(token)
    link = Link.create(
        url=request.form.get('url'),
        title=request.form.get('title'),
        description=request.form.get('description'),
        author=user
    )
    return jsonify({"success": True})


@links.route('/<int:linkid>', methods=['PUT'])
@owner_required
def update_link(linkid):
    """Update informations for link with given ID."""
    from waikup.models import Link
    link = Link.get(Link.id == linkid)
    link.safe_update(request.form)
    return jsonify({"success": True})


@links.route('/<int:linkid>', methods=['DELETE'])
@owner_required
def delete_link(linkid):
    """Delete link with given ID."""
    from waikup.models import Link
    try:
        delete_query = Link.delete().where(Link.id == linkid)
        delete_query.execute()
    except DoesNotExist:
        raise ApiError("Link not found: %d" % linkid, status_code=404)
    return jsonify({"success": True})
