import re
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.artworks = []  # probably won't use this either

####### Class Methods #######

    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL('lag_schema_v2.0').query_db(query, data)

    @classmethod
    def select_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('lag_schema_v2.0').query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])

    @classmethod
    def select_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(
            'lag_schema_v2.0').query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])

####### Static Methods #######

    @staticmethod
    def validate_registration(form_data):
        valid_entry = True
        if len(form_data['first_name']) < 1:
            valid_entry = False
            flash('First name must be longer than 3 characters', 'register')
        if len(form_data['last_name']) < 1:
            valid_entry = False
            flash('Last name must be longer than 3 characters', 'register')
        if not EMAIL_REGEX.match(form_data['email']):
            valid_entry = False
            flash("Please enter a valid email address", 'register')
        if len(form_data['password']) < 8:
            valid_entry = False
            flash('Password must be at least 8 characters long!', 'register')
        if form_data['password'] != form_data['confirm_password']:
            valid_entry = False
            flash('Passwords need to match', 'register')
        return valid_entry

    @staticmethod
    def validate_login(form_data):
        email_data = {
            "email": form_data['email']
        }
        user_found = User.select_user_by_email(email_data)
        if user_found == None:
            flash('credentials invalid invalid', 'login')
            return False
        if not bcrypt.check_password_hash(user_found.password, form_data['password']):
            flash("credentials invalid invalid", 'login')
            return False
        return user_found
