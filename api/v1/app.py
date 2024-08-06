#!/usr/bin/python3

from flask import Flask, make_response, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """Calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def error404(error):
    """custom error404 handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))

    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'

    app.run(host=host, port=port, threaded=True)