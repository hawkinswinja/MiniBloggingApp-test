from flask import Flask
from flasgger import Swagger
from routes import bp, redis_client, request, jsonify

app = Flask(__name__)
# app.config.from_pyfile('config.cfg')
app.url_map.strict_slashes = False

# Configure Flasgger
swagger = Swagger(app)
authenticated_urls = []  # urls requiring user authentication
# Register blueprints
app.register_blueprint(bp)


def authenticate_request():
    # Get the current request URL
    current_url = request.path

    # Check if the current URL requires authentication
    if current_url in authenticated_urls:
        # Check if the request contains an "Authorization" header with a token
        token = request.headers.get('Authorization')

        if not token:
            # If no token is provided, return an authentication error response
            return jsonify({'error': 'Authentication required'}), 401

        # Query the Redis instance to validate the token
        user_id = redis_client.get(token)

        if user_id:
            # If the token is valid, allow the request to proceed
            return None  # No authentication error

        # If the token is invalid, return an authentication error response
        return jsonify({'error': 'Invalid token'}), 401

    # If the URL doesn't require authentication, allow the request to proceed
    return None  # No authentication required for this URL


# Decorate the authentication function with Flask's before_request
@app.before_request
def run_authentication_check():
    auth_result = authenticate_request()

    if auth_result is not None:
        # Return the authentication error response
        return auth_result


if __name__ == "__main__":
    app.run(debug=True)
