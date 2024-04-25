#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """
    retrieves all State objects in json format
    """
    states_list = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        state_list.append(obj.to_json())

    return jsonify(state_list)


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    retrieves a State object by its ID
    """
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)

    return jsonify(state_obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """
    delete State by id
    """
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)

    storage.delete(state_obj)
    storage.save()

    return jsonify({})


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    create new State
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    res = jsonify(new_state.to_json())
    res.status_code = 201

    return res


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def put_state(state_id):
    """
    updates State object by ID
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, val)
    state_obj.save()
    return jsonify(state_obj.to_json())
