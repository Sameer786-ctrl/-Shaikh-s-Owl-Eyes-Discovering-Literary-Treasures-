from flask_app.config.mysqlconnection import connectToMySQL

import re
from flask import flash 

class User_Message:
    def __init__(self,data):
        self.user_id = data['user_id']
        self.message_id = data['message_id']
        self.from_id = data['from_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
