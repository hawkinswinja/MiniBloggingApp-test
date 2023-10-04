from flask import Flask
from flask_restplus import Api
from routes import views

# Create a Flask app instance
app = Flask(__name__)

# Load app configuration
app.config.from_object("config")

# Create an API instance
api = Api(app, version="1.0", title="Mini Blog API",
          description="Defines the Endpoints for Mini Blog Api")

# Register the status blueprint
app.register_blueprint(views)
