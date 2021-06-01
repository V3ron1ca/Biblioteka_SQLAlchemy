from app import db


class Book(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), index=True, unique=True)
   description = db.Column(db.String(200), index=True)
   done = db.Column(db.Boolean)
   author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

   def __str__(self):
       return f"<Book {self.title}>"


class Author(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), index=True, unique=True)
   surname = db.Column(db.String(100), index=True, unique=True)
   books = db.relationship("Book", backref="author", lazy="dynamic")

   def __str__(self):
       return f"<Author {self.name} {self.surname}>"