from .. import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    google_api_id = db.Column(db.String(255))
    isbn = db.Column(db.String(20))
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    published_date = db.Column(db.Date)

    # Define relationships
    # author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # Define back-references for relationships
    # author = db.relationship('Author', backref='books')
    # category = db.relationship('Category', backref='books')

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
