from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

#association table 
class UserBooks(db.Model):
    __tablename__ = 'user_books'

    id = db.Column(db.Integer ,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id' , ondelete="CASCADE"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id' , ondelete="CASCADE"), nullable=False)
    status = db.Column(db.Enum('reading', 'completed', 'pending'), nullable=False, default="reading")

    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id', name='unique_user_book'),
    )

    
    user = db.relationship("User", back_populates="user_books")
    book = db.relationship("Book", back_populates="user_books")
    collection_books = db.relationship("CollectionBooks", back_populates="user_book", cascade="all, delete-orphan")
    

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    
    user_books = db.relationship(
    "UserBooks",
    back_populates="user",
    cascade="all, delete-orphan")

    # cannot do this because now user_books is a association object nd secondary work only with pure junction table 
    # books = db.relationship("Book", secondary="user_books", back_populates="users") 

    collections = db.relationship(
    "UserCollection",
    back_populates="user",
    cascade="all, delete-orphan",
    passive_deletes=True)

    
    def set_hashed_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_hashed_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    title = db.Column(db.String(300), nullable=False)
    author_name = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    published_date = db.Column(db.String(50))
    description = db.Column(db.Text)
    page_count = db.Column(db.Integer)
    categories = db.Column(db.String(100))
    language = db.Column(db.String(100))
    info_link = db.Column(db.String(512))
    thumbnail = db.Column(db.String(512))
    isbn_13 = db.Column(db.String(13), unique=True, nullable=True)
    isbn_10 = db.Column(db.String(10), unique=True, nullable=True)

    
    user_books = db.relationship("UserBooks", back_populates="book")
  

class UserCollection(db.Model):
    __tablename__ = 'user_collection'

    collection_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id' ,ondelete="CASCADE"), nullable=False)
    collection_name = db.Column(db.String(50), nullable=False)

    
    user = db.relationship("User", back_populates="collections")
    collection_books = db.relationship(
    "CollectionBooks",
    back_populates="collection",
    cascade="all, delete-orphan")


class CollectionBooks(db.Model):
    __tablename__ = 'collection_books'

    collection_id = db.Column(db.Integer, db.ForeignKey('user_collection.collection_id' ,ondelete="CASCADE"), primary_key=True)
    user_book_id = db.Column(db.Integer, db.ForeignKey('user_books.id', ondelete="CASCADE"), primary_key=True)


    collection = db.relationship("UserCollection", back_populates="collection_books")
    user_book = db.relationship("UserBooks", back_populates="collection_books", passive_deletes=True)



class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_token'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    reset_token = db.Column(db.String(255),nullable=False)
    expires_at = db.Column(db.DateTime,nullable=False)
    token_used = db.Column(db.Boolean,nullable=False,default=False)