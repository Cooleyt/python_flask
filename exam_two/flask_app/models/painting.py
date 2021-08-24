from flask_app.config.mysqlconnection import MySQLConnection

from flask import flash

from flask_app import app
from flask_app.models.user import User

class Painting():

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None

    @classmethod
    def new_painting(cls, data):
        query = "INSERT INTO paintings (title, description, price, users_id) VALUES (%(title)s, %(description)s, %(price)s, %(users_id)s);"

        new_painting = MySQLConnection('exam_schema_two').query_db(query, data)

        return new_painting

    @classmethod
    def get_painting(cls, data):
        query = "SELECT * FROM paintings JOIN users ON paintings.users_id = users.id WHERE paintings.id = %(id)s;"

        results = MySQLConnection('exam_schema_two').query_db(query, data)

        painting = Painting(results[0])
        user_data = {
                'id': results[0]['users.id'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'email': results[0]['email'],
                'password': results[0]['password'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at']
        }
        painting.user = User(user_data)
        return painting

    @classmethod
    def get_all_paintings(cls):
        query = "SELECT * FROM paintings JOIN users ON paintings.users_id = users.id;"
        
        results = MySQLConnection('exam_schema_two').query_db(query)
        
        paintings = []

        for item in results:
            painting = Painting(item)
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
            painting.user = user
            paintings.append(painting)

        return paintings

    @classmethod
    def edit_painting(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s WHERE paintings.id = %(id)s;"

        edit_painting = MySQLConnection('exam_schema_two').query_db(query, data)

        return edit_painting

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM paintings WHERE paintings.id = %(id)s;"

        return MySQLConnection('exam_schema_two').query_db(query, data)

    @staticmethod
    def validate_painting(data):
        is_valid = True

        if len(data['title']) < 2 or len(data['title']) >46:
            is_valid = False
            flash('Title must be at least 2 characters long')
            
        if len(data['description']) < 10 or len(data['title']) >46:
            is_valid = False
            flash('Description must be at least 10 characters long')

        if len(data['price']) < 0:
            is_valid = False
            flash('Price must be greater than 0')

        return is_valid