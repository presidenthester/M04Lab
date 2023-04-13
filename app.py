from flask import Flask, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['DEBUG'] = True
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Book(id={self.id}, book_name='{self.book_name}', author='{self.author}', publisher='{self.publisher}')"

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.__dict__ for book in books]), 200

@app.route('/books', methods=['POST'])
def add_book():
    data = requests.get_json()
    book = Book(book_name=data['book_name'], author=data['author'], publisher=data['publisher'])
    db.session.add(book)
    db.session.commit()
    return jsonify(book.__dict__), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = requests.get_json()
    book.book_name = data['book_name']
    book.author = data['author']
    book.publisher = data['publisher']
    db.session.commit()
    return jsonify(book.__dict__), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204



