from flask import Flask
from flasgger import Swagger
from routes import bp  # Import the blueprint from the routes module

app = Flask(__name__)

# Configure Flasgger
swagger = Swagger(app)

# Register the users blueprint
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
