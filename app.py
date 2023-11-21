from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publisher = db.Column(db.String(80))
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.book_name} - {self.description}"


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'name': book.book_name, 'author': book.author, 'description': book.description,
                     'Publisher': book.publisher}

        output.append(book_data)
    return {'books': output}


@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"name": book.name, "description": book.description}


@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['name'], author=request.json['author'], description=request.json['description'],
                publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}


@app.route('/drinks/<id>', methods=['DELETE'])
def delete_book():
    book = Book.query.get(id)
    if book is None:
        return {'error 404': 'Not Found'}
    db.session.delete(book)
    db.session.commit()
    return {'message': 'Yeet!'}


if __name__ == '__main__':
    app.run()
