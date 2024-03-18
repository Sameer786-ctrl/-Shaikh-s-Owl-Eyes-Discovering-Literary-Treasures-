from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash 

from flask_app.models import address_model

class Host:
    def __init__(self,data):
        self.user_id = data['user_id']
        self.flock_id = data['flock_id']
        self.event_date = data['event_date']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def validate_host(host):
        is_valid = True # we assume this is true
        if len(host['new_host_id']) < 1:
            flash("Please pick a flock memeber to be the host","host")
            is_valid = False
        return is_valid

# =============================================
# CREATE: new host
# =============================================
    @classmethod
    def make_new_host(cls, data):
        query = "INSERT INTO hosts_users (user_id, flock_id, event_date) VALUES (%(user_id)s, %(flock_id)s, %(event_date)s);"
        results = connectToMySQL('book_club').query_db(query,data)
        return results

# =============================================
# SELECT : all open months for the group
# =============================================
    @classmethod
    def open_months(cls,data):
        query = "SELECT month FROM hosts_users WHERE flock_id = %(flock_id)s;"
        results = connectToMySQL('book_club').query_db(query,data)
        return results 

# =============================================
#Select : are you host?
# =============================================
    @classmethod
    def get_host_info(cls,data):
        query = "SELECT * FROM hosts_users LEFT JOIN address ON address.user_id = hosts_users.user_id = %(id)s;"
        results = connectToMySQL('book_club').query_db(query,data)

        host_info = []

        for row in results:
            one_host = cls(row)

            one_address = {
                "id" : row['id'],
                "address" : row['address'],
                "city" : row['city'],
                "state" : row['state'],
                "zip" : row['zip'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at']
            }
            one_host.address = address_model.Address(one_address)

            host_info.append(one_host)
        return host_info