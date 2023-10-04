from flask import jsonify, request
from routes import bp, storage, swag_from, redis_client, Auth  # Imported from __init__.py
from datetime import datetime


def get_current_date():
    """
    Get the current date in string format (YYYY-MM-DD).
    """
    current_date = datetime.now()
    return current_date.strftime('%Y-%m-%d')


def get_author_id():
    token = redis_client.get(request.headers.get('Authorization'))
    return token


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
    for post in posts:
        post['_id'] = str(post['_id'])
    return jsonify(posts), 200


@bp.route('/articles/<string:article_id>', methods=['GET'])
@swag_from(methods=['GET'])
def get_posts_by_id(article_id):
    """
    Get a post using its article_id.
    ---
    parameters:
      - name: article_id
        in: path
        type: string
        required: true
        description: article's ID.
    responses:
      200:
        description: Returns a posts by the specified id.
    """
    post = storage.find_post_by_id(article_id)
    post['_id'] = str(post['_id'])
    print(post)
    return jsonify(post), 200


@bp.route('/articles', methods=['POST'])
@swag_from(methods=['POST'])
def insert_article():
    """
    Insert a new article.
    ---
    parameters:
      - name: Authorization
        in: header
        description: The authorization token.
        required: true
        type: string
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
    # author_id = redis_client.get(request.headers.get('Authorization'))
    article_data = {
        "_id": Auth.get_token(),
        "title": request.form.get("title"),
        "content": request.form.get("content"),
        "author_id": get_author_id(),
        "created_at": get_current_date()
    }
    result = storage.insert_post(article_data)
    return jsonify(str(result.inserted_id)), 201


@bp.route('/articles/<string:article_id>', methods=['DELETE'])
@swag_from(methods=['DELETE'])
def delete_article(article_id):
    """
    Delete an article by its ID.
    ---
    parameters:
      - name: Authorization
        in: header
        description: The authorization token.
        required: true
        type: string
      - name: article_id
        in: path
        type: string
        required: true
        description: The ID of the article to delete.
    responses:
      204:
        description: The article was successfully deleted.
    """
    auth = False
    for post in storage.find_posts_by_author(get_author_id()):
        if str(post['_id']) == article_id:
            auth = True

    if auth:
        result = storage.delete_post(article_id)
        if result.deleted_count == 1:
            return "Article successfully deleted", 204
        else:
            return jsonify({"error": "Article not found"}), 404
    return 'Forbidden request', 403


@bp.route('/articles/<string:article_id>', methods=['PUT'])
@swag_from(methods=['PUT'])
def update_article_content(article_id):
    """
    Update the content of an article by its ID.
    ---
    parameters:
      - name: Authorization
        in: header
        description: The authorization token.
        required: true
        type: string
      - name: article_id
        in: path
        type: string
        required: true
        description: The id of the article to update.
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
    if article_id in storage.find_posts_by_author(get_author_id()):
        updated_data = {"content": request.form.get("content"),
                        "updated_at": get_current_date()}
        # id = request.form.get("article_id")
        result = storage.update_post(article_id, updated_data)
        if result.modified_count == 1:
            return jsonify({"message": "Article updated successfully"})
        else:
            return jsonify({"error": "Article not found"}), 404
    return "Forbidden request", 403
