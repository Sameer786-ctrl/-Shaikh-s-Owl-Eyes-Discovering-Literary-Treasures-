from flask_app.config.mysqlconnection import connectToMySQL

import re
from flask import flash 

from flask_app.models import flock_model
from flask_app.models import flock_user_model

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.phone = data['phone']
        self.email = data['email']
        self.password = data['password']
        self.profile_image = data['profile_image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("Frist name must be at least 3 characters.","error")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters.","error")
            is_valid = False
        if len(user['phone']) < 10:
            flash("Phone number mush be 10 characters long","error")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Last name must be at least 3 characters.","error")
            is_valid = False
        if len(user['password']) < 8:
            flash("password must be at least 8 characters long","error")
            is_valid = False
        if re.search('[0-9]',user['password']) is None:
            flash("Passwords must have a number","error")
            is_valid = False
        if re.search('[A-Z]',user['password']) is None:
            flash("Passwords must have a captial letter","error")
            is_valid = False
        if not user['password'] == user['confirm_password']:
            flash("Passwords must match","error")
            is_valid = False
        return is_valid

    def validate_update_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("Frist name must be at least 3 characters.","user")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters.","user")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Last name must be at least 3 characters.","user")
            is_valid = False
        if len(user['phone']) < 10:
            flash("Phone number mush be 10 characters long","user")
            is_valid = False
        return is_valid

    def validate_password(password):
        is_valid = True # we assume this is true
        if len(password['old_password']) < 8:
            flash("Old Password must be 8 characters long","password")
            is_valid = False
        if len(password['password']) < 8:
            flash("New password must be at least 8 characters long","password")
            is_valid = False
        if re.search('[0-9]',password['password']) is None:
            flash("New password must have a number","password")
            is_valid = False
        if re.search('[A-Z]',password['password']) is None:
            flash("New password must have a captial letter","password")
            is_valid = False
        if not password['password'] == password['confirm_password']:
            flash("Passwords must match")
            is_valid = False
        return is_valid
    

# ==========================================
# SELECT: all users
# ==========================================
    @classmethod
    def get_all_users(cls,data):
        query = "SELECT * FROM users WHERE id != %(id)s ORDER BY first_name;"
        results = connectToMySQL('book_club').query_db(query,data)

        users = []

        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def user_user_info(cls,data):
        query =  "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return cls(results[0])

# ========================================
# SELECT: admin user for goup
# ========================================
    @classmethod
    def user_by_id(data):
        query =  "SELECT * FROM flocks LEFT JOIN groups_users ON flocks.id = groups_users.flock_id LEFT JOIN users ON users.id = groups_users.user_id WHERE flocks.id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ========================================
# SELECT: one user info with group info
# ========================================
    @classmethod
    def get_user_info(cls,data):
        query = "SELECT *  FROM users  LEFT JOIN flocks_users  ON users.id = flocks_users.user_id  LEFT JOIN flocks ON flocks_users.flock_id = flocks.id  LEFT JOIN address ON address.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)

        users_information = []

        for row in results:
            one_user = cls(row)

            flock_data = {
                "id" :  row['flocks.id'],
                "title" :  row['title'],
                "city" :  row['city'],
                "state" :  row['state'],
                "privacy_setting" :  row['privacy_setting'],
                "created_at" :  row['flocks.created_at'],
                "updated_at" :  row['flocks.updated_at']
            }
            one_user.flock = flock_model.Flock(flock_data)

            address_data = {
                "id": row['address.id'],
                "address": row['address'],
                "city": row['address.city'],
                "state": row['address.state'],
                "zip": row['zip'],
                "created_at": row['address.created_at'],
                "updated_at": row['address.updated_at']
            }
            one_user.address = address_model.Address(address_data)

            one_status = {
                "id": row['flocks_users.id'],
                "user_id": row['user_id'],
                "flock_id": row['flock_id'],
                "status": row['status'],
                "created_at": row['flocks_users.created_at'],
                "updated_at": row['flocks_users.updated_at']
            }
            one_user.info = flock_user_model.Flock_User(one_status)

            users_information.append(one_user)
        return users_information

# ============================================= 
# SELECT : all data from a single flock (changed name from  get_all_flock_info to get_all_users_in_flock in case something breaks)
# ============================================= 
    @classmethod
    def get_all_users_in_flock(cls,data):
        query = "SELECT * FROM users LEFT JOIN flocks_users ON flocks_users.user_id = users.id LEFT JOIN flocks ON flocks.id = flocks_users.flock_id WHERE users.id = %(id)s AND flocks_users.status != 'admin';"
        results = connectToMySQL('book_club').query_db(query,data)

        all_flock_info = []

        for row in results:
            one_user = cls(row)

            one_flock_user = {
                "id" : row['id'],
                "user_id" : row['user_id'],
                "flock_id" : row['flock_id'],
                "status" : row['status'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at']
            }
            one_user.flur = flock_user_model.Flock_User(one_flock_user)

            one_flock = {
                "id" : row['id'],
                "title" : row['title'],
                "city" : row['city'],
                "state" : row['state'],
                "privacy_setting" : row['privacy_setting'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at']
            }
            one_user.flock = flock_model.Flock(one_flock)

            all_flock_info.append(one_user)
        return all_flock_info

# ========================================
# SELECT all users in flock
# ========================================
    @classmethod
    def all_flock_users(cls,data):
        query = "SELECT * FROM users  LEFT JOIN  flocks_users ON flocks_users.user_id = users.id  LEFT JOIN flocks ON flocks.id = flocks_users.flock_id  WHERE flocks_users.status != 'admin' AND flocks.id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)

        all_flock_info = []

        for row in results:
            one_user = cls(row)

            one_flock_user = {
                "id" : row['flocks_users.id'],
                "user_id" : row['user_id'],
                "flock_id" : row['flock_id'],
                "status" : row['status'],
                "created_at" : row['flocks_users.created_at'],
                "updated_at" : row['flocks_users.updated_at']
            }
            one_user.flur = flock_user_model.Flock_User(one_flock_user)

            one_flock = {
                "id" : row['id'],
                "title" : row['title'],
                "city" : row['city'],
                "state" : row['state'],
                "privacy_setting" : row['privacy_setting'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at']
            }
            one_user.flock = flock_model.Flock(one_flock)

            all_flock_info.append(one_user)
        return all_flock_info

# ========================================
# CREATE: new user
# ========================================   
    @classmethod
    def create_new_user(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ========================================  
# UPDATE: message count
# ========================================  
    @classmethod
    def increment_messge_cout(cls,data):
        query = "UPDATE users SET message_count = message_count + 1 WHERE id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ========================================  
# UPDATE: user info
# ========================================  
    @classmethod
    def update_user_info(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s,email = %(email)s,phone = %(phone)s  WHERE id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ========================================  
# UPDATE: password
# ========================================  
    @classmethod
    def update_current_assword(cls,data):
        query = "UPDATE users SET password = %(password)s  WHERE id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ========================================
# VALIDATION: by uer email
# ========================================
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        if not results:
            return "0"
        else:        
            return cls(results[0])

# ========================================
# VALIDATION: by user password
# ========================================
    @classmethod
    def get_by_password(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return cls(results[0])

# ========================================
# DELETE : user
# ========================================
    @classmethod
    def delete_user(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results