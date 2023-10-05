from pymongo import MongoClient
from datetime import datetime
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def get_current_date():
    """
    Get the current date in string format (YYYY-MM-DD).
    """
    current_date = datetime.now()
    return current_date.strftime('%Y-%m-%d  %H:%M:%S')


class Database:
    def __init__(self):
        self.client = MongoClient(getenv('MONGODB_URI'))
        self.db = self.client[getenv('MONGODB_DB')]
        self.users_collection = self.db['users']
        self.posts_collection = self.db['posts']

    def find_posts_by_author(self, author_id=None):
        "return list of posts on success"
        try:
            if author_id:
                posts = list(self.posts_collection.find({"author_id": author_id}))
            else:
                posts = list(self.posts_collection.find())
        except Exception as e:
            print(f"author id invalid: {e}")
            return []  # Return an empty list as a default in case of an error
        return posts

    def insert_user(self, user_data):
        from routes.auth import Auth
        user_data['_id'] = Auth.get_token()
        try:
            user = self.users_collection.insert_one(user_data)
            return user
        except Exception as e:
            print(f"Error inserting user: {e}")
            return

    def find_user_by_username(self, username):
        try:
            user = self.users_collection.find_one({"username": username})
        except Exception as e:
            print(f"Error finding user: {e}")
            return 1
        return user

    def insert_post(self, post_data):
        from routes.auth import Auth
        post_data["_id"] = Auth.get_token()
        post_data["created_at"] = get_current_date()
        try:
            post = self.posts_collection.insert_one(post_data)
        except Exception as e:
            print(f"Error inserting post: {e}")
            post = None
        return post

    def find_post_by_id(self, post_id):
        try:
            post = self.posts_collection.find_one({"_id": post_id})
        except Exception as e:
            print(f"Error finding post: {e}")
            post = None
        return post

    def update_post(self, post_id, updated_data):
        updated_data["updated_at"] = get_current_date()
        try:
            post = self.posts_collection.update_one({"_id": post_id},
                                                    {"$set": updated_data})
        except Exception as e:
            print(f"Error updating post: {e}")
            post = None
        return post

    def delete_post(self, post_id):
        try:
            result = self.posts_collection.delete_one({"_id": post_id})
        except Exception as e:
            print(f"Error deleting post: {e}")
            result = None
        return result
