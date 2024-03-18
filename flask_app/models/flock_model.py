from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash 

from flask_app.models import flock_user_model
from flask_app.models import user_model
from flask_app.models import host_model

class Flock:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.city = data['city']
        self.state = data['state']
        self.privacy_setting = data['privacy_setting']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def validate_flock(flock):
        is_valid = True # we assume this is true
        if len(flock['title']) < 2:
            flash("Please name your flock, it must be atleast 3 characters.","flocks")
            is_valid = False
        if len(flock['city']) < 2:
            flash("Please select a city","flocks")
            is_valid = False
        if len(flock['state']) < 2:
            flash("Please select a state","flocks")
            is_valid = False
        return is_valid

    def validate_new_admin(admin):
        is_valid = True # we assume this is true
        if len(admin['new_admin_id']) < 2:
            flash("Umm...why hit update if you didn't pick a new admin?","admin")
            is_valid = False
        return is_valid

# =============================================  
# SELECT: all groups with open privacy settings open
# =============================================
    @classmethod
    def select_all_flocks(cls,data):
        # make sure we're only getting admins, we're only getting the ones we didn't create, and we're making sure they're privacy setting is open
        query = "SELECT * FROM flocks LEFT JOIN flocks_users ON flocks_users.flock_id = flocks.id WHERE flocks.privacy_setting = 'open' AND flocks_users.user_id != %(id)s AND flocks_users.status = 'admin';"
        results = connectToMySQL('book_club').query_db(query,data)


        users_information = []

        for row in results:
            one_user = cls(row)

            one_status = {
                "id": row['flocks_users.id'],
                "user_id": row['user_id'],
                "flock_id": row['flock_id'],
                "status": row['status'],
                "created_at": row['flocks_users.created_at'],
                "updated_at": row['flocks_users.updated_at']
            }
            one_user.status = flock_user_model.Flock_User(one_status)

            users_information.append(one_user)
        return users_information

# =============================================
# SELECT : all flock info
# =============================================
    @classmethod
    def get_all_flock_info(cls,data):
        query = "SELECT * FROM flocks LEFT JOIN flocks_users  ON flocks.id = flocks_users.user_id  LEFT JOIN  users ON 	users.id = flocks_users.user_id WHERE flocks_users.flock_id = %(id)s AND status = 'admin';"
        results = connectToMySQL('book_club').query_db(query,data)

        flocks_information = []

        for row in results:
            one_flock = cls(row)

            one_status = {
                "id": row['flocks_users.id'],
                "user_id": row['user_id'],
                "flock_id": row['flock_id'],
                "status": row['status'],
                "created_at": row['flocks_users.created_at'],
                "updated_at": row['flocks_users.updated_at']
            }
            one_flock.info = flock_user_model.Flock_User(one_status)

            one_member = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "phone" : row['phone'],
                "email" : row['email'],
                "password" : row['password'],
                "profile_image" : row['profile_image'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at']
            }
            one_flock.member = user_model.User(one_member)

            flocks_information.append(one_flock)
        return flocks_information

# =============================================  
# SELECT: all flock info with a certain user id
# =============================================
    @classmethod
    def get_admin_info(cls,data):
        query =  "SELECT * FROM flocks LEFT JOIN flocks_users ON flocks_users.flock_id = flocks.id LEFT JOIN users ON users.id = flocks_users.user_id WHERE flocks_users.user_id = %(id)s;"
        
        results = connectToMySQL('book_club').query_db(query,data)
        
        flock_information = []

        for row in results:
            one_flock = cls(row)

            one_flock_user = {
                "id": row['flocks_users.id'],
                "user_id": row['user_id'],
                "flock_id": row['flock_id'],
                "status": row['status'],
                "created_at": row['flocks_users.created_at'],
                "updated_at": row['flocks_users.updated_at']
            }
            one_flock.status = flock_user_model.Flock_User(one_flock_user)

            one_user = {
                "id" : row['id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "phone" : row['phone'],
                "email" : row['email'],
                "phone" : row['phone'],
                "password" : row['password'],
                "profile_image" : row['profile_image'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at']
            }
            one_flock.member = user_model.User(one_user)

            flock_information.append(one_flock)
        return flock_information

# =============================================
# SELECT : all flock memebers who aren't the admin 
# =============================================
    @classmethod
    def get_flock_admin_info(cls,data):
        query =  "SELECT * FROM flocks LEFT JOIN flocks_users ON flocks_users.flock_id = flocks.id LEFT JOIN users ON users.id = flocks_users.user_id WHERE flocks_users.flock_id =  %(id)s AND flocks_users.status = 'admin';"
        
        results = connectToMySQL('book_club').query_db(query,data)
        
        flock_information = []

        for row in results:
            one_flock = cls(row)

            one_flock_user = {
                "id": row['id'],
                "user_id": row['user_id'],
                "flock_id": row['flock_id'],
                "status": row['status'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            one_flock.status = flock_user_model.Flock_User(one_flock_user)

            one_user = {
                "id" : row['id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "phone" : row['phone'],
                "email" : row['email'],
                "phone" : row['phone'],
                "password" : row['password'],
                "profile_image" : row['profile_image'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at']
            }
            one_flock.member = user_model.User(one_user)

            flock_information.append(one_flock)
        return flock_information

# ============================================= 
# SELECT : one flock 
# ============================================= 
    @classmethod
    def get_flock_info(cls,data):
        query = "SELECT * FROM flocks WHERE id = %(flock_id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# =============================================  
# SELECT: check if group name is unique
# =============================================
    @classmethod
    def unique_flock_name(cls,data):
        query = "SELECT * FROM flocks WHERE title = %(title)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# =============================================  
# SELECT: whether user is admin
# =============================================
    @classmethod
    def get_user_admin(cls,data):
        query =  "SELECT users.first_name,users.last_name,flocks.title,flocks_users.status,flocks_users.created_at AS start,flocks_users.flock_id,flocks_users.user_id FROM flocks_users LEFT JOIN flocks ON flocks.id = flocks_users.flock_id LEFT JOIN users ON users.id = flocks_users.user_id WHERE users.id = %(id)s AND flocks_users.status = 'admin'";
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# =============================================  
# CREATE: new flock
# =============================================
    @classmethod
    def save_flock(cls,data):
        query = "INSERT INTO flocks (title, city, state, privacy_setting) VALUES (%(title)s, %(city)s, %(state)s, %(privacy_setting)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# =============================================
# INSERT: creator as the admin
# =============================================
    @classmethod
    def make_creator_admin(cls,data):
        query = "INSERT INTO flocks_users (flock_id,user_id,status) VALUES (%(flock_id)s , %(user_id)s,'admin')"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# =============================================
# DELETE: from group
# =============================================
    @classmethod
    def remove_from_flock(cls,data):
        query = "DELETE FROM flocks_users WHERE  flock_id = %(flock_id)s AND user_id = %(user_id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# =============================================
# UPDATE : change admin
# =============================================
    @classmethod
    def remove_old_admin(cls,data):
        query = "UPDATE flocks_users SET status = 'user'  WHERE  user_id = %(old_admin_id)s AND flock_id = %(flock_id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results 

    @classmethod
    def make_new_admin(cls,data):
        query = "UPDATE flocks_users SET status = %(type)s WHERE  user_id = %(user_id)s AND flock_id = %(flock_id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results 