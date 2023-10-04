from flask import Flask
from flask_testing import TestCase
from routes.posts_routes import bp  # Import your blueprint here
from db import Database  # Import your Database class here


class TestPostsRoutes(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.register_blueprint(bp)
        return app

    def setUp(self):
        self.db = Database()
        self.db.client.drop_database(self.db.db.name)

    def test_get_all_posts(self):
        # Insert some test posts into the database
        post_data1 = {
            "title": "Test Post 1",
            "content": "Content 1",
            "author_id": "author1",
            "created_at": "2023-10-10T12:00:00Z",
        }
        post_data2 = {
            "title": "Test Post 2",
            "content": "Content 2",
            "author_id": "author2",
            "created_at": "2023-10-11T12:00:00Z",
        }
        self.db.insert_post(post_data1)
        self.db.insert_post(post_data2)

        # Send a GET request to /articles
        response = self.client.get('/articles')

        # Check if the response status code is 200 (OK)
        self.assert200(response)

    def test_insert_article(self):
        # Send a POST request to insert a new article
        new_article_data = {
            "title": "New Article",
            "content": "This is a new article",
            "created_at": "2023-10-12T12:00:00Z",
        }
        response = self.client.post('/articles/author1', data=new_article_data)

        # Check if the response status code is 201 (Created)
        self.assertStatus(response, 201)

        # Check if the response data contains the ID of the newly created article
        new_article_id = response.json
        self.assertTrue(new_article_id)
        # Check if the article is actually inserted into the database
        inserted_article = self.db.find_post_by_id(new_article_id)
        self.assertEqual(inserted_article["title"], new_article_data["title"])

    def test_delete_article(self):
        # Insert a test post into the database
        post_data = {
            "title": "Test Post",
            "content": "Content",
            "author_id": "author1",
            "created_at": "2023-10-10T12:00:00Z",
        }
        result = self.db.insert_post(post_data)

        # Get the ID of the inserted post
        post_id = str(result.inserted_id)

        # Send a DELETE request to /articles/<post_id>
        response = self.client.delete(f'/articles/{post_id}')

        # Check if the response status code is 204 (No Content)
        self.assertStatus(response, 204)

        # Check if the post is deleted from the database
        deleted_post = self.db.find_post_by_id(post_id)
        self.assertIsNone(deleted_post)

    def test_update_article_content(self):
        # Insert a test post into the database
        post_data = {
            "title": "Test Post",
            "content": "Content",
            "author_id": "author1",
            "created_at": "2023-10-10T12:00:00Z",
        }
        result = self.db.insert_post(post_data)

        # Get the ID of the inserted post
        post_id = str(result.inserted_id)
        # Send a PUT request to /articles/<post_id>
        updated_content = {
            "content": "Updated Content",
        }
        response = self.client.put(f'/articles/{post_id}',
                                   data=updated_content)

        # Check if the response status code is 200 (OK)
        self.assert200(response)

        # Check if the post in the database has the updated content
        updated_post = self.db.find_post_by_id(post_id)
        self.assertEqual(updated_post["content"], updated_content["content"])

    def tearDown(self):
        # Clean up the test database after each test
        self.db.client.drop_database(self.db.db.name)

# if __name__ == '__main__':
#     unittest.main()
