from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash 

class Book_Author:
    def __init__(self,data):
        self.book_id = data['book_id']
        self.author_id = data['author_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# ============================================= 
# INSERT : new book / author ids
# ============================================= 
    @classmethod
    def add_new_book_author(cls,data):
        query = "INSERT INTO books_authors (book_id,author_id) VALUES (%(book_id)s, %(author_id)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results