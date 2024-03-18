from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash 

class Book_Series:
    def __init__(self,data):
        self.id = data['id']
        self.book_id = data['book_id']
        self.series_id = data['series_id']
        self.num = data['num']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# =============================================  
# SELECT : check for unique book series
# =============================================  
    @classmethod
    def is_series_order_unique(cls,data):
        query = "SELECT * FROM book_series_number WHERE book_id = %(book_id)s AND series_id = %(series_id)s AND num = %(num)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# =============================================  
# add book and series
# =============================================  
    @classmethod
    def add_book_to_series(cls,data):
        query = "INSERT INTO book_series_number (book_id,series_id,num) VALUES (%(book_id)s,%(series_id)s,%(num)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

    