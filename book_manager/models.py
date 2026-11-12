
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    books = db.relationship(
        "Book",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category {self.name}>"

class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publish_year = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=0, nullable=False)

    # Foreign Key
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=False
    )

    # Relationship
    category = db.relationship(
        "Category",
        back_populates="books"
    )

    def __repr__(self):
        return f"<Book {self.title}>"
