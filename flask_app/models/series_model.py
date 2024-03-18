from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash 

class Series:
    def __init__(self,data):
        self.id = data['id']
        self.series_name = data['series_name']
        self.book_id = data['book_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# ============================================= 
# SELECT : is series unique
# ============================================= 
    @classmethod
    def is_series_unique(cls,data):
        query = "SELECT * FROM book_series WHERE series_name = %(series_name)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ============================================= 
# SELECT : get exsisting series id
# ============================================= 
    @classmethod
    def get_series_id(cls,data):
        query = "SELECT id FROM book_series WHERE series_name = %(series_name)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ============================================= 
# SELECT : all series
# ============================================= 
    @classmethod
    def get_all_series(cls):
        query = "SELECT * FROM book_series ORDER BY series_name ASC;"
        results = connectToMySQL('book_club').query_db(query)
        return results
        
# ============================================= 
# INSERT : add new series 
# ============================================= 
    @classmethod
    def add_new_series(cls,data):
        query = "INSERT INTO book_series (series_name) VALUES(%(series_name)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results


