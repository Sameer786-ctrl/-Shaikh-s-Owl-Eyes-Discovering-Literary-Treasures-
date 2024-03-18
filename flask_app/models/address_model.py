from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash 

class Address:
    def __init__(self,data):
        self.id = data['id']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def validate_update_address(address):
        is_valid = True # we assume this is true
        if len(address['address']) < 3:
            flash("Address must be at least 3 characters.","address")
            is_valid = False
        if len(address['city']) < 3:
            flash("City must be at least 3 characters.","address")
            is_valid = False
        if len(address['state']) < 3:
            flash("Please choose a state","address")
            is_valid = False
        if len(address['zip']) < 5:
            flash("Zip must be 5 characters long","address")
            is_valid = False
        return is_valid

# ========================================  
# SELECT: if user has an address
# ======================================== 
    @classmethod
    def has_address(cls,data):
        query = "SELECT * FROM address WHERE user_id = %(user_id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        if len(results) < 1:
            return '0'
        else:
            return results

# ========================================  
# CREATE: new address
# ========================================  
    @classmethod
    def add_address(cls,data):
        query = "INSERT INTO address (address,state,city,zip,user_id) VALUES ( %(address)s, %(state)s, %(city)s, %(zip)s, %(user_id)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# ========================================  
# UPDATE: address
# ========================================  
    @classmethod
    def update_address(cls,data):
        query = "UPDATE address SET address = %(address)s, state = %(state)s, city = %(city)s, zip = %(zip)s WHERE user_id = %(user_id)s"
        results = connectToMySQL('book_club').query_db(query,data)
        return results
# ============================================= 
# DELETE : address
# ============================================= 
    @classmethod
    def delete_user_address(cls,data):
        query = "DELETE FROM address WHERE user_id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results