from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
     
        
    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO user (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)'
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        return results
    
    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM user WHERE email = %(email)s'
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if not results:
            return None
        
        return User(results[0])
    
    @classmethod
    def return_first_name(cls, data):
        query = 'SELECT first_name FROM user WHERE email = %(email)s'
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if not results:
            return None
        
        return results[0]['first_name']
    
    @classmethod
    def return_id(cls, data):
        query = 'SELECT id FROM user WHERE email = %(email)s'
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if not results:
            return None
        
        return results[0]['id']
        
    @staticmethod
    def validate_user(user):
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        is_valid = True
        
        if (regex.search(user['first_name']) != None or len(user['first_name']) < 2):
            # first name contains special characters
            flash('First name contains special characters or does not meet minimum length requirements.', "registration")
            is_valid = False
        
        if (regex.search(user['last_name'])!= None or len(user['last_name']) < 2):
            # last name contains special characters
            flash('Last name contains special characters or does not meet minimum length requirements.', "registration")
            is_valid = False
        
        if (len(user['password']) < 8):
            # password is too short
            flash('Password is too short', "registration")
            is_valid = False
            
        if (re.search('[0-9]', user['password']) == None):
            # password does not contain digits
            flash('Password does not contain digits', "registration")
            is_valid = False
            
        if (re.search('[A-Z]', user['password']) == None):
            # password does not contain uppercase letters
            flash('Password does not contain a uppercase letters', "registration")
            is_valid = False
            
        if (regex.search(user['password']) == None):
            # password contains not special characters
            flash('Password contains not a special characters', "registration")
            is_valid = False
        
        if (user['password']!= user['password_confirmation']):
            flash('Passwords do not match', "registration")
            is_valid = False
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if (re.fullmatch(regex, user['email'])):
            # email is valid
            # need to check if the email is already in use
            this_user = {
                'email': user['email']
            }
            results = User.check_database(this_user)
            
            if len(results) != 0:
                flash('Email is already in use, please use a different email', "registration")
                is_valid = False
        else:
            flash('Email contains special characters', "registration")
            is_valid = False
        
        return is_valid
    
    @classmethod
    def check_database(cls, data):
        query = "SELECT * FROM user WHERE user.email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        print(len(results))
        
        return results