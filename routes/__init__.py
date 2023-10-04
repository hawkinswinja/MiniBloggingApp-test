from flask import Blueprint, jsonify
from flasgger import swag_from
from db import Database


storage = Database()
bp = Blueprint("blog", __name__)


@bp.route('/status', methods=['GET'])
@swag_from(methods=['GET'])  # Specify documentation comes from docstrings
def status():
    """
    Get the status of the API.
    ---
    responses:
      200:
        description: Success, the API is up and running.
    """
    return jsonify({"status": "success"})


from routes.posts_routes import *
