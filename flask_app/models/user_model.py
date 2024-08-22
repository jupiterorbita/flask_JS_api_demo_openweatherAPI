# models talk to the DB
from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import DATABASE
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
        self.updated_at = data['updated_at']


    # ------- CREATE user --------
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
            """
        return connect_to_mysql(DATABASE).query_db(query, data)
    
    # ------ READ ONE (GET BY EMAIL) -----------
    @classmethod
    def get_by_email(cls, email):
        data = {
            'email' : email
        }
        query = """
            SELECT * FROM users
            WHERE email = %(email)s;
            """
        results = connect_to_mysql(DATABASE).query_db(query, data)
        print("\n ??????? DID WE GET A USER BACK ?????", results)
        if len(results) < 1:
            return False
        return cls(results[0])

    #  ---------------- READ ONE - GET BY ID ---------------
    @classmethod
    def get_by_id(cls, id):
        data = {
            'id' : id
        }
        query = """
            SELECT * FROM users
            WHERE id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query, data)
        print("\n ??????? DID WE GET A USER BACK ?????", results)
        if len(results) < 1:
            return False
        return User(results[0])

    # ======== VALIDATIONS =========
    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['first_name']) < 1:
            is_valid = False
            flash("first_name is required", 'reg')
        
        if len(data['last_name']) < 1:
            is_valid = False
            flash("last_name is required", 'reg')
        
        if len(data['email']) < 1:
            is_valid = False
            flash("email is required" , 'reg')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Invalid email address!!!!" , 'reg')
        else :
            potential_user = User.get_by_email(data['email'])
            if potential_user:
                is_valid = False
                flash("email is taken... hopefully by you!", 'reg')
        
        if len(data['password']) < 1:
            is_valid = False
            flash("password is required" , 'reg')
        elif not data['password'] == data['confirm_password']:
            is_valid = False
            flash("passwords must match!" , 'reg')



        return is_valid

        