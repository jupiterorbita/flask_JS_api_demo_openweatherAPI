# models talk to the DB
from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model

class Party:
    def __init__(self, data):
        self.id = data['id']
        self.what = data['what']
        self.location = data['location']
        self.date = data['date']
        self.all_ages = data['all_ages']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # self.planner = None

    # ------------ CREATE PARTY -----------
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO parties
                (what, location, date, all_ages, description, user_id)
            VALUES 
                (%(what)s ,%(location)s ,%(date)s ,%(all_ages)s ,%(description)s ,%(user_id)s );
            """
        return connect_to_mysql(DATABASE).query_db(query, data)
    
    # ----------------- READ ALL  parties and thier creator / user -----
    @classmethod
    def get_all_parties(cls):
        query = """
                SELECT * FROM parties
                JOIN users
                ON parties.user_id = users.id;
            """
        results = connect_to_mysql(DATABASE).query_db(query)
        print("*********get_all_parties ==> RESULTS :\n", results)

        list_of_all_parties = []
        for row in results:
            # create the Party instance
            this_party = cls(row)

            # now create the data dict for the User constructor
            user_data = {
                **row,
                'id' : row['users.id'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            # now create the user
            this_user = user_model.User(user_data)

            # add a new attribute to the Party
            this_party.planner = this_user

            list_of_all_parties.append(this_party)
        return list_of_all_parties
    

    # ------------- READ ONE party -------------
    @classmethod
    def get_by_id(cls, id):
        data = {
            'id' : id
        }
        query = """
            SELECT * FROM parties
            JOIN users
            ON users.id = parties.user_id
            WHERE parties.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query, data)
        print("*********get_by_id ==> RESULTS :\n", results) # [{}]
        
        if results:
            # create the party:
            this_party = cls(results[0])

            # create the user for the party
            row = results[0]
            user_data = {
                **row,
                'id' : row['users.id'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            this_user = user_model.User(user_data)

            this_party.planner = this_user
            return this_party
        return False


    # ----------- UPDATE a party -------------
    @classmethod
    def update(cls, data):
        query = """
            UPDATE parties
            SET
                what = %(what)s,
                location = %(location)s,
                date = %(date)s,
                all_ages = %(all_ages)s,
                description = %(description)s
            WHERE id = %(id)s;
        """
        return connect_to_mysql(DATABASE).query_db(query, data)
    


    # ====== PARTY VALIDATOR ==========
    def validate(form_data):
        is_valid = True

        if len(form_data['what']) < 1:
            is_valid = False
            flash("what is required")

        if len(form_data['location']) < 1:
            is_valid = False
            flash("where is required")

        if len(form_data['date']) < 1:
            is_valid = False
            flash("enter a date")

        if len(form_data['description']) < 1:
            is_valid = False
            flash("description is required")

        if 'all_ages' not in form_data:
            is_valid = False
            flash("please select for all ages")
        
        return is_valid