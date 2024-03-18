from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash 

class Genre:
    def __init__(self,data):
        self.id = data['id']
        self.genre = data['genre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# ==========================================
# SELECT : check to see if genre exsists
# ==========================================
    @classmethod
    def genre_exsist(cls,data):
        query = "SELECT id FROM genre WHERE genre = %(genre)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ==========================================
# SELECT : genre by an id
# ==========================================
    @classmethod
    def genre_get_exsisting_id(cls,data):
        query = "SELECT id FROM genre WHERE genre = %(genre)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ==========================================
# SELECT : all genres in db
# ==========================================
    @classmethod
    def get_all_genres(cls):
        query = "SELECT * FROM genre ORDER BY genre ASC;"
        results = connectToMySQL('book_club').query_db(query)
        return results

# ==========================================
# INSERT: new genre
# ==========================================
    @classmethod
    def add_new_genre(cls,data):
        query = "INSERT INTO genre (genre) VALUES (%(genre)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results