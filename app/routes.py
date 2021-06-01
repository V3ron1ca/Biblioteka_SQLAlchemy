from . import app, db
from .models import Author, Book
from flask import abort, make_response, request, jsonify


@app.route("/api/v1/books/", methods=["GET"])
def books_list_api_v1():
    return jsonify([{ "id" : book.id, "title" : book.title, "description" : book.description, "done" : book.done, "author_id" : book.author_id } for book in Book.query.all()])


@app.route("/api/v1/authors/", methods=["GET"])
def authors_list_api_v1():
    return jsonify([{ "id" : author.id, "name" : author.name, "surname" : author.surname } for author in Author.query.all()])


@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)
    return jsonify(id=book.id,
                   title=book.title,
                   description=book.description,
                   done=book.done,
                   author_id=book.author_id)


@app.route("/api/v1/authors/<int:author_id>", methods=["GET"])
def get_author(author_id):
    author = Author.query.get(author_id)
    if not author:
        abort(404)
    return jsonify([{ "id" : author.id, "name" : author.name, "surname" : author.surname } for author in Author.query.all()])


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.route("/api/v1/books/", methods=["POST"])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = Book(title=request.json['title'], description=request.json['description'], done=False, author_id=request.json["author_id"])
    db.session.add(book)
    db.session.commit()
    return jsonify(id=book.id,
                   title=book.title,
                   description=book.description,
                   done=book.done,
                   author_id=book.author_id), 201


@app.route("/api/v1/auhtors/", methods=["POST"])
def create_author():
    if not request.json or not 'title' in request.json:
        abort(400)
    author = Author(name=request.json['name'], surname= request.json['surname'])
    db.session.add(author)
    db.session.commit()
    return jsonify([{ "id" : author.id, "name" : author.name, "surname" : author.surname } for author in Author.query.all()]), 201


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    book.title = data.get('title', book.title)
    book.description = data.get('description', book.description)
    book.done = data.get('done', book.done)
    book.author_id = data.get('author_id', book.author_id)
    db.session.add(book)
    db.session.commit()
    return jsonify(id=book.id,
                   title=book.title,
                   description=book.description,
                   done=book.done,
                   author_id=book.author_id)


@app.route("/api/v1/authors/<int:author_id>", methods=["PUT"])
def update_author(author_id):
    author = Author.query.get(author_id)
    if not author:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'name' in data and not isinstance(data.get('name'), str),
        'surname' in data and not isinstance(data.get('surname'), str)
    ]):
        abort(400)
    author.name = data.get('name', author.name)
    author.surname = data.get('surname', author.surname)
    db.session.add(author)
    db.session.commit()
    return jsonify([{ "id" : author.id, "name" : author.name, "surname" : author.surname } for author in Author.query.all()])