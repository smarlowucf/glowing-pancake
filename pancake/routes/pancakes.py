import json

from flask import Blueprint, jsonify, request, make_response

from pancake import utils

blueprint = Blueprint('pancakes', __name__, url_prefix='/pancakes')


@blueprint.route('/version', methods=['GET'])
def get_version():
    return make_response(jsonify({'version': '1.0.0'}), 200)

@blueprint.route('/', methods=['POST'])
def add_pancake():
    data = json.loads(request.data.decode())

    try:
        utils.add_pancake_type(data)
    except Exception as error:
        msg = 'Unable to add pancake: {0}'.format(error)
        return make_response(jsonify({'msg': msg}), 400)

    return make_response(jsonify({'msg': 'Pancake added'}), 201)


@blueprint.route('/', methods=['GET'])
def get_pancakes():
    try:
        types = utils.get_pancake_types()
    except Exception as error:
        msg = 'Unable to retrieve pancake types: {0}'.format(error)
        return make_response(jsonify({'msg': msg}), 400)

    return make_response(jsonify(types), 200)


@blueprint.route('/<name>', methods=['GET'])
def get_pancake(name):
    try:
        pancake = utils.get_pancake(name)
    except Exception as error:
        msg = 'Unable to retrieve pancake: {0}'.format(error)
        return make_response(jsonify({'msg': msg}), 400)

    return make_response(jsonify(pancake), 200)


@blueprint.route('/<name>', methods=['DELETE'])
def delete_pancake(name):
    try:
        utils.delete_pancake_type(name)
    except Exception as error:
        msg = 'Unable to delete pancake: {0}'.format(error)
        return make_response(jsonify({'msg': msg}), 400)

    return make_response(jsonify({'msg': 'Pancake deleted'}), 200)
