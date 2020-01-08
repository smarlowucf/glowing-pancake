import json

from flask import current_app


def add_pancake_type(data):
    types = get_pancake_types_from_db()
    types[data['name']] = {'ingredients': data['ingredients']}
    save_pancake_types_db(types)


def get_pancake_types():
    return get_pancake_types_from_db()


def get_pancake(name):
    types = get_pancake_types_from_db()
    return types[name]


def delete_pancake_type(name):
    types = get_pancake_types_from_db()
    del types[name]
    save_pancake_types_db(types)


def get_pancake_types_from_db():
    db = current_app.config['PANCAKE_DB']

    with open(db) as f:
        types = json.load(f)

    return types


def save_pancake_types_db(types):
    db = current_app.config['PANCAKE_DB']

    with open(db, 'w') as f:
        json.dump(types, f, indent=2)
