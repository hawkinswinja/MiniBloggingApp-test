from bson.json_util import dumps
from flask import jsonify, request
from . import bp, storage, swag_from  # Imported from __init__.py
from datetime import datetime


def get_current_date():
    """
    Get the current date in string format (YYYY-MM-DD).
    """
    current_date = datetime.now()
    return current_date.strftime('%Y-%m-%d')


# GET /articles - returns a list of all saved posts
@bp.route('/articles', methods=['GET'])
@swag_from(methods=['GET'])
def get_all_posts():
    """
    Get all posts.
    ---
    responses:
      200:
        description: Returns a list of all posts.
    """
    posts = storage.find_posts_by_author()
    return jsonify(posts)


# returns a list of posts with the given author_id
@bp.route('/articles/<string:author_id>', methods=['GET'])
@swag_from(methods=['GET'])
def get_posts_by_author(author_id):
    """
    Get posts by author.
    ---
    parameters:
      - name: author_id
        in: path
        type: string
        required: true
        description: The author's ID.
    responses:
      200:
        description: Returns a list of posts by the specified author.
    """
    posts = storage.find_posts_by_author(author_id)
    return jsonify(posts)


# POST /articles/<str:author_id> - inserts the article to the db
@bp.route('/articles/<string:author_id>', methods=['POST'])
@swag_from(methods=['POST'])
def insert_article(author_id):
    """
    Insert a new article.
    ---
    parameters:
      - name: author_id
        in: path
        type: string
        required: true
        description: The author's ID.
      - name: title
        in: formData
        type: string
        required: true
        description: The title of the article.
      - name: content
        in: formData
        type: string
        required: true
        description: The content of the article.
    responses:
      201:
        description: id of the newly created article.
    """
    article_data = {
        "title": request.form.get("title"),
        "content": request.form.get("content"),
        "author_id": author_id,
        "created_at": get_current_date()
    }
    result = storage.insert_post(article_data)
    return jsonify(str(result.inserted_id)), 201


# DELETE /articles/<str:author_id> - delete an article using article_id
@bp.route('/articles/<string:article_id>', methods=['DELETE'])
@swag_from(methods=['DELETE'])
def delete_article(article_id):
    """
    Delete an article by its ID.
    ---
    parameters:
      - name: article_id
        in: path
        type: string
        required: true
        description: The ID of the article to delete.
    responses:
      204:
        description: The article was successfully deleted.
    """
    result = storage.delete_post(article_id)
    if result.deleted_count == 1:
        return "Article successfully deleted", 204
    else:
        return jsonify({"error": "Article not found"}), 404


# PUT /articles/<str:author_id> - update the content of an article
@bp.route('/articles/<string:article_id>', methods=['PUT'])
@swag_from(methods=['PUT'])
def update_article_content(article_id):
    """
    Update the content of an article by its ID.
    ---
    parameters:
      - name: article_id
        in: path
        type: string
        required: true
        description: The ID of the article to update.
      - name: content
        in: formData
        type: string
        required: true
        description: The updated content of the article.
    responses:
      200:
        description: successful update.
      404:
        description: article not found
    """
    updated_data = {"content": request.form.get("content"),
                    "updated_at": get_current_date()}
    result = storage.update_post(article_id, updated_data)
    if result.modified_count == 1:
        return jsonify({"message": "Article updated successfully"})
    else:
        return jsonify({"error": "Article not found"}), 404
