from flask_app.config.mysqlconnection import connectToMySQL

import re
from flask import flash 

from flask_app.models import user_model
from flask_app.models import user_message_model
from flask_app.models import flock_model

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')

class Message:
    def __init__(self,data):
        self.id = data['id']
        self.message = data['message']
        self.message_type = data['message_type']
        self.subject = data['subject']
        self.from_id = data['from_id']
        self.flock_id = data['flock_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def validate_message(message):
        is_valid = True # we assume this is true
        if len(message['message']) < 10:
            flash("Message must be longer than 10 characters","message")
            is_valid = False
        if message["flock_id"] == "0":
            flash("Must choose a Group","message")
            is_valid = False
        return is_valid

    def validate_send_message(message):
        is_valid = True # we assume this is true
        if len(message['subject']) < 3:
            flash("Please add a subject that is atleast 3 characters.","personal")
            is_valid = False
        if len(message['message']) < 3:
            flash("If you have no message why are you sending one?","personal")
            is_valid = False
        return is_valid

# SELECT: get all messages
    @classmethod
    def get_messages(cls,data):
        query = " SELECT * FROM messages LEFT JOIN users_messages ON users_messages.message_id = messages.id LEFT JOIN flocks ON flocks.id = messages.flock_id WHERE users_messages.user_id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)

        users_messages = []

        for row in results:
            one_user = cls(row)

            one_message_info = {
                "user_id" : row['user_id'],
                "message_id" : row['message_id'],
                "subject" : row['subject'],
                "from_id" : row['from_id'],
                "flock_id" : row['flock_id'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at']
            }
            one_user.info = user_message_model.User_Message(one_message_info)

            one_flock_info = {
                "id": row['flocks.id'],
                "title": row['title'],
                "city": row['city'],
                "state": row['state'],
                "privacy_setting": row['privacy_setting'],
                "created_at": row['flocks.created_at'],
                "updated_at": row['flocks.updated_at']
            }

            one_user.flock = flock_model.Flock(one_flock_info)

            users_messages.append(one_user)
        return users_messages

# =============================================
# DELETE : user's messages
# =============================================
    @classmethod
    def delete_user_messages(cls,data):
        query = "DELETE FROM users_messages WHERE user_id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# =============================================
# INSERT: request to join group
# =============================================
    @classmethod
    def save_message(cls, data):
        query = "INSERT INTO messages (message,message_type,from_id,flock_id) VALUE (%(message)s,%(message_type)s,%(from_id)s,%(flock_id)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ==========================================
# INSERT: save who it's forrm and who it's for
# ==========================================
    @classmethod
    def save_to_from_info(cls,data):
        query = "INSERT INTO users_messages (user_id,message_id) VALUES (%(user_id)s, %(message_id)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ==========================================
# Saving a personal message
# ==========================================
    @classmethod
    def save_new_message(cls,data):
        query = "INSERT INTO messages (from_id,subject,message_type,message) VALUES (%(user_id)s,%(subject)s,%(message_type)s,%(message)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# =============================================
# DELETE: message
# =============================================
    @classmethod
    def delete_message(cls,data):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results
    
    @classmethod
    def delete_user_message(cls,data):
        query = "DELETE FROM users_messages WHERE user_id = %(user_id)s AND message_id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results