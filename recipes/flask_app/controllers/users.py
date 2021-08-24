from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_bcrypt import Bcrypt 

from flask_app.models.user import User
from flask_app.models.recipe import Recipe

bcrypt = Bcrypt(app) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/register', methods=['POST'])
def register_user():
    #first validate users names, emails, passwords.
    # print(User.validate_user(request.form)) -- to test
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        (request.form['password'])
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        id = User.create_user(data)
        session['user_id'] = id
        flash("You are now registered, you can log in!")
    return redirect('/')

@app.route('/users/login', methods = ['POST'])
def login():

    users = User.get_user_by_first_name(request.form)

    if len(users) != 1:
        flash('First name or password is incorrect')
        return redirect('/')

    user = users[0]

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password is incorrect.')
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.firstname
    
    flash('Name/password correct')
    return redirect('/dashboard')

@app.route('/user/logout')
def logout():
    session.clear()
    flash("You've logged out")
    return redirect('/')



