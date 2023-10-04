import bcrypt
import uuid


class Auth:
    @staticmethod
    def hash_password(plain_password):
        # Generate a salt and hash the plain_password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode(), salt)
        return hashed_password.decode()

    @staticmethod
    def validate(plain_password, hashed_password):
        # Check if the plain_password matches the hashed_password
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

    @staticmethod
    def get_token():
        # Generate a short UUIDv4 token
        token = str(uuid.uuid4())[:8]
        return token
