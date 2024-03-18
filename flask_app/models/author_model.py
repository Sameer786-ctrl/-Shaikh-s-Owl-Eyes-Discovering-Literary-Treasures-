from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash 

class Author:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# =============================================  
# SELECT: is author unique
# =============================================  
    @classmethod
    def is_author_unique(cls,data):
        query = "SELECT * FROM authors WHERE first_name = %(first_name)s AND last_name = %(last_name)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# =============================================  
# SELECT: get author ID
# =============================================  
    classmethod
    def get_author_id(cls,data):
        query = "SELECT * FROM authors WHERE first_name = %(first_name)s AND last_name = %(last_name)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return cls(results[0])

# =============================================  
# INSERT: new author
# =============================================     
    @classmethod
    def add_new_author(cls,data):
        query = "INSERT INTO authors (first_name,last_name) VALUES (%(first_name)s, %(last_name)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

