from flask_app.config.mysqlconnection import MySQLConnection
import re

from flask import flash

from flask_app import app

class User():

    def __init__(self, data):
        self.id = data['id']
        self.firstname = data['first_name']
        self.lastname = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'

        result = MySQLConnection('exam_schema_two').query_db(query, data)

        return result

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = MySQLConnection('exam_schema_two').query_db(query, data)

        users= []

        for line in results:
            users.append(User(line))

        return users

    @classmethod
    def get_user_by_first_name(cls, data):
        query = 'SELECT * FROM users WHERE first_name = %(first_name)s;'
        results = MySQLConnection('exam_schema_two').query_db(query, data)
        users= []

        for line in results:
            users.append(User(line))

        return users

    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT * FROM users WHERE users.id = %(id)s;'
        results= MySQLConnection('exam_schema_two').query_db(query, data)
        return cls(results[0])


    @staticmethod
    def validate_user(data):
        is_valid = True

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(data['first_name']) < 2 or len(data['first_name']) >46:
            is_valid = False
            flash('First name must be at least 2 characters long')

        if len(data['last_name']) < 2 or len(data['last_name']) >46:
            is_valid = False
            flash('Last name must be at least 2 characters long')

        if not email_regex.match(data['email']):
            is_valid = False
            flash('Email is not in the correct format')

        if len(data['email']) > 255:
            is_valid = False
            flash('Email must be under 255 characters')

        if len(User.get_user_by_email(data)) > 0:
            is_valid = False
            flash('Email is already in use')

        if len(data['password'])  < 8:
            is_valid = False
            flash('Password must be at least 8 characters long')

        if not data['password'] == data['confirm_password']:
            is_valid = False
            flash('Passwords do not match')

        return is_valid
