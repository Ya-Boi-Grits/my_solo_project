from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


class Achievement:
    def __init__(self, data):
        self.id = data['id'],
        self.name = data['name'],
        self.description = data['description'],
        self.points = data['points'],
        self.users_id = None

####### Class Methods #######

    @classmethod
    def add_achievement_to_db(cls, data):
        query = "INSERT INTO achievements (name, description, points, users_id) VALUES (%(name)s,%(description)s,%(points)s,%(id)s);"
        return connectToMySQL('lag_schema_v2.0').query_db(query, data)

    @classmethod
    def update_achievement_by_id(cls, data):
        query = "UPDATE achievements SET name = %(name)s,description = %(description)s,points = %(points)s WHERE id = %(id)s"
        return connectToMySQL('lag_schema_v2.0').query_db(query, data)

    @classmethod
    def get_all_achievements_from_db(cls):
        query = "SELECT * FROM achievements;"
        results = connectToMySQL('lag_schema_v2.0').query_db(query)
        print(results)
        if len(results) == 0:
            return None
        else:
            return results

    @classmethod
    def get_achievement_by_id(cls, data):
        query = "SELECT * FROM achievements WHERE id = %(id)s;"
        results = connectToMySQL('lag_schema_v2.0').query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else:
            return results[0]

    @classmethod
    def delete_achievement_by_id(cls, data):
        query = "DELETE FROM achievements WHERE id = %(id)s;"
        return connectToMySQL('lag_schema_v2.0').query_db(query, data)

####### Static Methods #######

    @staticmethod
    def validate_add_achievement(form_data):
        validate_entry = True
        if len(form_data['name']) < 4:
            validate_entry = False
            flash('Achievement name must be at least 4 characters long', 'achievement')
        if len(form_data['description']) < 10:
            validate_entry = False
            flash('Sorry, your description is too short', 'achievement')
        # if (form_data['points']) < 10:
        #     validate_entry = False
        #     flash('Your achievement must be worth at least 10 points', 'achievement')
        # if (form_data['points']) > 500:
        #     validate_entry = False
        #     flash("Nothing can be worth that many points....", 'achievement')
        return validate_entry
