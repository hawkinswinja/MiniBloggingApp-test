from flask import Blueprint
from flask_restx import Resource, Namespace

blog_ns = Namespace("blog")
blog_bp = Blueprint("blog", __name__)

@blog_ns.route("/")
def get(self):
    return {"status": "success"}, 200

