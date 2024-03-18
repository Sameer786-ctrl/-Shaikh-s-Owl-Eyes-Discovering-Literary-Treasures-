from flask_app.config.mysqlconnection import connectToMySQL

import re
from flask import flash 


class Flock_User:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.flock_id = data['flock_id']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# ========================================
# INSERT : new user into flock
# ========================================
    @classmethod
    def add_user_to_flock(cls,data):
        query = "INSERT INTO flocks_users (user_id,flock_id) VALUES (%(user_id)s,%(flock_id)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

    