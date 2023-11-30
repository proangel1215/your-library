from .. import db


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


books_authors_table = db.Table(
    "books_authors",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id")),
    db.Column("author_id", db.Integer, db.ForeignKey("authors.id")),
)


books_categories_table = db.Table(
    "books_categories",
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id")),
    db.Column("book_id", db.Integer, db.ForeignKey("books.id")),
)


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    google_api_id = db.Column(db.String(255))
    isbn = db.Column(db.String(20))
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    published_date = db.Column(db.Date)
    
    
    authors = db.relationship(
        "Author", secondary=books_authors_table, backref="books")

    categories = db.relationship(
        "Category", secondary=books_categories_table, backref="books")

    def __init__(
        self,
        title,
        isbn,
        author,
        category,
        published_date,
        description,
        image_url,
        google_api_id,
    ):
        self.title = title
        self.isbn = isbn
        self.author = author
        self.category = category
        self.published_date = published_date
        self.description = description
        self.image_url = image_url
        self.google_api_id = google_api_id

    # def as_dict(self):
    #     return {
    #         'title': self.title,
    #         'isbn': self.isbn,
    #         'author': self.author.name if self.author else None,
    #         'category': self.category.name if self.category else None
    #     }
