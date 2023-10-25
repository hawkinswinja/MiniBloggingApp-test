from flask import Flask
from flasgger import Swagger
from routes import bp, redis_client, request, jsonify

app = Flask(__name__)
# app.config.from_pyfile('config.cfg')
app.url_map.strict_slashes = False

# Configure Flasgger
swagger = Swagger(app)  # urls requiring user authentication
# Register blueprints
app.register_blueprint(bp)


@app.before_request
def authenticate_request():
    if 'articles' in request.path and request.method in ['POST', 'PUT', 'DELETE']:
        token = request.headers.get('Authorization')

        if not token:
            # If no token is provided, return an authentication error response
            return jsonify({'error': 'Authentication required'}), 401

        # Query the Redis instance to validate the token
        user_id = redis_client.get(token)

        if not user_id:
            # If the token is invalid, return an authentication error response
            return jsonify({'error': 'Invalid token'}), 401

    # Allow the request to proceed
    return None


if __name__ == "__main__":
    app.run(debug=True)
