import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

########################################################################################################
# Models
########################################################################################################

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Add a role column for RBAC
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }

class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    books = db.relationship('Book', backref='section', lazy=True)
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date_created': self.date_created
        }

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'pages': self.pages,
            'volume': self.volume
        }

class BookRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'request_date': self.request_date,
            'return_date': self.return_date
        }

class IssuedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True, default=None)
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'issue_date': self.issue_date,
            'return_date': self.return_date
        }


########################################################################################################
# User Routes
########################################################################################################

# route "user-login" to match username and password and return user details. RBAC based login
@app.route('/user-login', methods=['POST'])
def user_login():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "username and password required"}), 400
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify({"error": "invalid username or password"}), 400
    # Check the role and return based on that
    if user.role == 'user' or user.role == 'librarian':
        return jsonify(user.serialize())
    else:
        return jsonify({"error": "invalid role"}), 400

# route "user-register" to add new user if username or email is not already taken
@app.route('/user-register', methods=['POST'])
def user_register():
    data = request.json
    if 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({"error": "username, password and email are required"}), 400
    # if anything has empty value, return error
    if not data['username'] or not data['password'] or not data['email']:
        return jsonify({"error": "username, password and email are required"}), 400
    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({"error": "username already taken"}), 400
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({"error": "email already taken"}), 400
    user = User(username=data['username'], password=data['password'], email=data['email'], role='user')
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

# route "request-book" to request a book by user. Request will have username and book_id
@app.route('/user-request-book', methods=['POST'])
def request_book():
    print(request)
    data = request.json
    if 'username' not in data or 'book_id' not in data:
        return jsonify({"error": "username and book_id required"}), 400
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({"error": "user not found"}), 404
    book = Book.query.get(data['book_id'])
    if not book:
        return jsonify({"error": "book not found"}), 404
    book_request = BookRequest(user_id=user.id, book_id=book.id)
    db.session.add(book_request)
    db.session.commit()
    return jsonify(book_request.serialize())

# route "user-all-books" to get all books
@app.route('/user-all-books')
def user_all_books():
    books = Book.query.all()
    books = list(map(lambda book: book.serialize(), books))
    return jsonify(books)

# route "user-my-books/<int:user_id>" to get all books issued to a user. 
# returns "completed": [list of books returned] and "currentlyIssued": [list of books currently issued]
@app.route('/user-my-books/<string:username>')
def user_my_books(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "user not found"}), 404
    user_id = user.id
    completed = db.session.query(IssuedBook, Book).join(Book).filter(IssuedBook.return_date != None, IssuedBook.user_id == user_id).all()
    completed = list(map(lambda issued_book: issued_book.Book.serialize(), completed))
    currently_issued = db.session.query(IssuedBook, Book).join(Book).filter(IssuedBook.return_date.is_(None), IssuedBook.user_id == user_id).all()
    currently_issued = list(map(lambda issued_book: issued_book.Book.serialize(), currently_issued))
    return jsonify({"completed": completed, "currentlyIssued": currently_issued})


########################################################################################################
# Librarian Routes
########################################################################################################

# route "librarian-login" to match username and password and return user details. RBAC based login
@app.route('/librarian-login', methods=['POST'])
def librarian_login():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "username and password required"}), 400
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify({"error": "invalid username or password"}), 400
    if user.role != 'librarian':
        return jsonify({"error": "unauthorised access"}), 400
    return jsonify(user.serialize())

# route "librarian-add-section" to add new section
@app.route('/librarian-add-section', methods=['POST'])
def librarian_add_section():
    data = request.json
    if 'name' not in data or 'description' not in data:
        return jsonify({"error": "name and description required"}), 400
    section = Section(name=data['name'], description=data['description'])
    db.session.add(section)
    db.session.commit()
    return jsonify(section.serialize())

# route "librarian-delete-section/<int:section_id>" to delete section by id
@app.route('/librarian-delete-section/<int:section_id>', methods=['DELETE'])
def librarian_delete_section(section_id):
    section = Section.query.get(section_id)
    if not section:
        return jsonify({"error": "section not found"}), 404
    # delete all books in the section
    books = Book.query.filter_by(section_id=section_id).all()
    for book in books:
        db.session.delete(book)
    # now delete the section
    db.session.delete(section)
    db.session.commit()
    return jsonify({"message": "section deleted"})

# route "librarian-all-sections" to get all sections
@app.route('/librarian-all-sections')
def librarian_all_sections():
    sections = Section.query.all()
    sections = list(map(lambda section: section.serialize(), sections))
    return jsonify(sections)

# route "librarian-add-book" to add new book
@app.route('/librarian-add-book/<int:section_id>', methods=['POST'])
def librarian_add_book(section_id):
    data = request.json
    if 'title' not in data or 'author' not in data or 'pages' not in data or 'volume' not in data:
        return jsonify({"error": "title, author, pages and volume required"}), 400
    section = Section.query.get(section_id)
    if not section:
        return jsonify({"error": "section not found"}), 404
    book = Book(title=data['title'], author=data['author'], pages=data['pages'], volume=data['volume'], section_id=section_id)
    db.session.add(book)
    db.session.commit()
    return jsonify(book.serialize())

# route "librarian-list-of-books/<int:section_id>" to get all books in a section
@app.route('/librarian-list-of-books/<int:section_id>')
def librarian_list_of_books(section_id):
    section = Section.query.get(section_id)
    if not section:
        return jsonify({"error": "section not found"}), 404
    books = Book.query.filter_by(section_id=section_id).all()
    books = list(map(lambda book: book.serialize(), books))
    return jsonify(books)

# route "librarian-book-requests" to get all book requests joined with user and book details
@app.route('/librarian-book-requests')
def librarian_book_requests():
    requests = db.session.query(BookRequest, User, Book).join(User).join(Book).all()
    requests = list(map(lambda request: {
        'id': request.BookRequest.id,
        'title': request.Book.title,
        'author': request.Book.author,
        'sectionName': request.Book.section.name,
        'requestedby': request.User.username,
        'numBooksToRequester': db.session.query(IssuedBook).filter_by(user_id=request.User.id).count()
    }, requests))
    return jsonify(requests)

# route "librarian-approve-request/<int:request_id>" to approve a book request
@app.route('/librarian-approve-request/<int:request_id>', methods=['POST'])
def librarian_approve_request(request_id):
    request = BookRequest.query.get(request_id)
    if not request:
        return jsonify({"error": "request not found"}), 404
    issued_book = IssuedBook(user_id=request.user_id, book_id=request.book_id, issue_date=datetime.datetime.utcnow())
    db.session.add(issued_book)
    db.session.delete(request)
    db.session.commit()
    return jsonify(issued_book.serialize())

# route "librarian-reject-request/<int:request_id>" to reject a book request
@app.route('/librarian-reject-request/<int:request_id>', methods=['POST'])
def librarian_reject_request(request_id):
    request = BookRequest.query.get(request_id)
    if not request:
        return jsonify({"error": "request not found"}), 404
    db.session.delete(request)
    db.session.commit()
    return jsonify({"message": "request rejected"})

########################################################################################################
# Helper Routes
########################################################################################################

@app.route('/')
def index():
    # return "accessible" in json
    return jsonify({"message": "accessible"})

# route "users" to get all users 
@app.route('/users')
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users)

# route "sections" to get all sections
@app.route('/sections')
def get_sections():
    sections = Section.query.all()
    sections = list(map(lambda section: section.serialize(), sections))
    return jsonify(sections)

# route "books" to get all books
@app.route('/books')
def get_books():
    books = Book.query.all()
    books = list(map(lambda book: book.serialize(), books))
    return jsonify(books)

# route "book-requests" to get all book requests
@app.route('/book-requests')
def get_book_requests():
    requests = BookRequest.query.all()
    requests = list(map(lambda request: request.serialize(), requests))
    return jsonify(requests)

# route "issued-books" to get all issued books
@app.route('/issued-books')
def get_issued_books():
    issued_books = IssuedBook.query.all()
    issued_books = list(map(lambda issued_book: issued_book.serialize(), issued_books))
    return jsonify(issued_books)

# route "add-user" to add new user if username or email is not already taken
@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.json
    if 'username' not in data or 'password' not in data or 'email' not in data or 'role' not in data:
        return jsonify({"error": "username, password, email and role are required"}), 400
    if not data['username'] or not data['password'] or not data['email'] or not data['role']:
        return jsonify({"error": "username, password, email and role are required"}), 400
    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({"error": "username already taken"}), 400
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({"error": "email already taken"}), 400
    user = User(username=data['username'], password=data['password'], email=data['email'], role=data['role'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

# route "delete-user" to delete user by id
@app.route('/delete-user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "user deleted"})

# route "delete-book" to delete book by id
@app.route('/delete-book/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "book deleted"})

########################################################################################################
# Entry point
########################################################################################################

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)