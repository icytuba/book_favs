from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.num_of_pages = db_data['num_of_pages']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.authors = []
    
    @classmethod
    def save_book(cls, data):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(np)s);"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def all_books(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL('books_schema').query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books

    @classmethod
    def one_book(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN \
            users ON favorites.user_id = users.id WHERE books.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query, data)
        book = cls(results[0])
        for db_row in results:
            author_data ={
                'id': db_row['users.id'],
                'name': db_row['name'],
                'created_at': db_row['users.created_at'],
                'updated_at': db_row['users.updated_at']
            }
            book.authors.append(author.Author(author_data))
        return book

    @staticmethod
    def fav(data):
        query= "INSERT INTO favorites (book_id, user_id) VALUES (%(book_id)s, %(user_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)