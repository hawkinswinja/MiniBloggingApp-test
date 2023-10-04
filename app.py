from flask import Flask
# from config.py import Config  # Import your app's configuration
from models.db import Database  # Import the Database class

app = Flask(__name__)
# app.config.from_object(Config)  # Load your app's configuration

db = Database()  # Initialize the database
result = db.insert_post({"post": "hello testing12345"})
print(result.get("_id"))

# Define your routes and other app configurations here

if __name__ == "__main__":
    app.run(debug=True)
