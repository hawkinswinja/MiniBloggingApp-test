import unittest
from db import Database


class TestDatabase(unittest.TestCase):

    # Successfully insert a user into the database
    def test_insert_user_success(self):
        # Create a mock user data
        user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "password123"
        }
        # Insert the user into the database
        db = Database()
        result = db.insert_user(user_data)
        print(result.inserted_id)
        # Check if the user was inserted successfully
        self.assertIsNotNone(result.inserted_id)

    # Successfully find a user by their username
    def test_find_user_by_username_success(self):
        # Create a mock user data
        user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "password123"
        }
        # Insert the user into the database
        db = Database()
        db.insert_user(user_data)

        # Find the user by their username
        result = db.find_user_by_username("test_user")

        # Check if the user was found successfully
        self.assertIsNotNone(result)

    # Successfully insert a post into the database
    def test_insert_post_success(self):
        # Create a mock post data
        post_data = {
            "title": "Test Post",
            "content": "This is a test post"
        }

        # Insert the post into the database
        db = Database()
        result = db.insert_post(post_data)

        # Check if the post was inserted successfully
        self.assertIsNotNone(result.inserted_id)

    # Attempt to find a user by a username that does not exist
    def test_find_user_by_username_not_found(self):
        # Find a user by a username that does not exist
        db = Database()
        result = db.find_user_by_username('non-existent_user')

        # Check if the user was not found
        self.assertIsNone(result)

    # Attempt to find a post by an ID that does not exist
    def test_find_post_by_id_not_found(self):
        # Find a post by an ID that does not exist
        db = Database()
        result = db.find_post_by_id('non-existent_post')

        # Check if the post was not found
        self.assertIsNone(result)

    # Successfully find a post by its ID
    def test_find_post_by_id_success(self):
        # Create a mock post data
        post_data = {
            "title": "Test Post",
            "content": "This is a test post"
        }

        # Insert the post into the database
        db = Database()
        result = db.insert_post(post_data)

        # Find the post by its ID
        post_id = result.inserted_id
        found_post = db.find_post_by_id(post_id)
        print('post _id: ', found_post['_id'])

        # Check if the post was found successfully
        self.assertEqual(found_post["_id"], post_id)

    # Successfully update a post's data
    def test_update_post_success(self):
        # Create a mock post data
        post_data = {
            "title": "Test Post",
            "content": "This is a test post"
        }

        # Insert the post into the database
        db = Database()
        result = db.insert_post(post_data)

        # Update the post's data
        updated_data = {
            "title": "Updated Post",
            "content": "This is an updated post"
        }
        db.update_post(result.inserted_id, updated_data)

        # Find the updated post by its ID
        updated_post = db.find_post_by_id(result.inserted_id)

        # Check if the post was updated successfully
        self.assertEqual(updated_post["title"], updated_data["title"])
        self.assertEqual(updated_post["content"], updated_data["content"])

    # Successfully delete a post from the database
    def test_delete_post_success(self):
        # Create a mock post data
        post_data = {
            "title": "Test Post",
            "content": "This is a test post"
        }

        # Insert the post into the database
        db = Database()
        result = db.insert_post(post_data)

        # Delete the post from the database
        db.delete_post(result.inserted_id)

        # Try to find the deleted post by its ID
        deleted_post = db.find_post_by_id(result.inserted_id)

        # Check if the post was deleted successfully
        self.assertIsNone(deleted_post)
