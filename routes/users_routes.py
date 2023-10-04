from flask import jsonify, request
from . import bp, storage, swag_from, redis_client
from auth import Auth



@bp.route('/register', methods=['POST'])
@swag_from(methods=['POST'])
def register_user():
    """
    Register a new user.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
        description: The user's email.
      - name: username
        in: formData
        type: string
        required: true
        description: The desired username.
      - name: password
        in: formData
        type: string
        required: true
        description: The user's password.
    responses:
      201:
        description: User registered successfully.
      400:
        description: Bad request, user registration failed.
    """
    data = request.form
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # Hash the password before storing it
    hashed_password = Auth.hash_password(password)

    # Store the user information using the Database instance
    user_data = {'email': email, 'username': username,
                 'password': hashed_password}
    result = storage.insert_user(user_data)

    if result:
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'error': 'User registration failed'}), 400


@bp.route('/login', methods=['POST'])
@swag_from(methods=['POST'])
def login_user():
    """
    Authenticate and log in a user.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        description: The user's email.
      - name: username
        in: formData
        type: string
        description: The user's username.
      - name: password
        in: formData
        type: string
        required: true
        description: The user's password.
    responses:
      200:
        description: User logged in successfully, returns user token.
      401:
        description: Unauthorized, authentication failed.
    """
    data = request.form
    # email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # Find the user in the database using the Database instance
    user = storage.find_user_by_username(username)

    if user and Auth.validate(password, user['password']):
        # Generate a token and store it in Redis
        token = Auth.get_token()
        redis_client.set(token, username)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Authentication failed'}), 401


@bp.route('/logout', methods=['GET'])
@swag_from(methods=['GET'])
def get(self):
    """
    Log out the current user by deleting their token from Redis.
    responses:
      200:
        description: A message indicating successful logout.
    """
    token = request.headers.get('Authorization')
    if token:
        redis_client.delete(token)
    return jsonify({'message': 'Logout success'}), 200
