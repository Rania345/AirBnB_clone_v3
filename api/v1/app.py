#!/usr/bin/python3
""" App instance """

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """After each request call teardown function"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """ handles 404 errors """
    status = {
        "error": "Not found"
    }

    res = jsonify(status)
    res.status_code = 404

    return(res)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
