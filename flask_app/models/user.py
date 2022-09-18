from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash 
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.created_at = data['created_at']

#Register classmethods
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users ( first_name, last_name, email, password, created_at, updated_at ) VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s, NOW(), NOW() );'
        return connectToMySQL('login_and_registration').query_db(query, data)

#Register staticmethods
    @staticmethod
    def validate_registration(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters long.")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters long.")
            is_valid = False
        if len(data['email']) < 2:
            flash("Invalid email address.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long.")
        if not data['password'] == data['password_confirmation']:
            flash("Password and Password Confirmation do not match.")
            is_valid = False
        return is_valid

#Login classmethods
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_and_registration").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

#Session classmethods
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("login_and_registration").query_db(query,data)
        return cls(result[0])