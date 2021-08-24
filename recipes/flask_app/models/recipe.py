from flask_app.config.mysqlconnection import MySQLConnection
import re

from flask import flash

from flask_app import app
from flask_app.models.user import User

class Recipe():

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.date = data['date']
        self.description = data['description']
        self.instruction = data['instruction']
        self.timing = data['timing']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None

    @classmethod
    def new_recipe(cls, data):
        query = "INSERT INTO recipes (name, date, description, instruction, timing, users_id) VALUES (%(name)s, %(date)s, %(description)s, %(instruction)s, %(timing)s, %(users_id)s);"

        new_recipe = MySQLConnection('recipes_schema').query_db(query, data)

        return new_recipe

    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"

        results = MySQLConnection('recipes_schema').query_db(query, data)

        return results

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.users_id = users.id;"
        
        results = MySQLConnection('recipes_schema').query_db(query)
        
        recipes = []

        for item in results:
            recipe = Recipe(item)
            user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            user = User(user_data)
            recipe.user = user
            recipes.append(recipe)

        return recipes




    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, date = %(date)s, description = %(description)s, timing = %(timing)s, instruction = %(instruction)s WHERE recipes.id = %(id)s;"

        edit_recipe = MySQLConnection('recipes_schema').query_db(query, data)

        return edit_recipe

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s;"

        return MySQLConnection('recipes_schema').query_db(query, data)