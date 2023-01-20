from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.books = []
    
    @classmethod
    def save_author(cls, data):
        query = "INSERT INTO users (name) VALUES (%(name)s);"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def all_authors(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('books_schema').query_db(query)
        authors = []
        for author in results:
            authors.append(cls(author))
        return authors
    
    @classmethod
    def one_author(cls, data):
        query = "SELECT * FROM users LEFT JOIN favorites ON favorites.user_id = users.id LEFT JOIN \
            books ON favorites.book_id = books.id WHERE users.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query, data)
        author = cls(results[0])
        for db_row in results:
            book_data ={
                'id': db_row['books.id'],
                'title': db_row['title'],
                'num_of_pages': db_row['num_of_pages'],
                'created_at': db_row['books.created_at'],
                'updated_at': db_row['books.updated_at']
            }
            author.books.append(book.Book(book_data))
        return author