from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_bcrypt import Bcrypt 

from flask_app.models.user import User
from flask_app.models.painting import Painting

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Log in to view this page')
        return redirect('/')

    return render_template('dashboard.html', paintings = Painting.get_all_paintings())

@app.route('/new/painting')
def new_painting():
    if 'user_id' not in session:
        flash('Log in to view this page')
        return redirect('/')
    return render_template('new_painting.html')


@app.route('/create/painting', methods=['POST'])
def create_painting():
    if Painting.validate_painting(request.form):
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'price': request.form['price'],
            'users_id': session['user_id']
        }
        painting_id = Painting.new_painting(data)
        print(painting_id)

        return redirect('/dashboard')
    return redirect('/new/painting')

@app.route('/paintings/<int:painting_id>')
def get_painting(painting_id):
    if 'user_id' not in session:
        flash('Log in to view this page')
        return redirect('/')
    data ={
        'id': painting_id
    }
    
    painting = Painting.get_painting(data)
    
    return render_template('show_painting.html', painting = painting)



@app.route('/paintings/<int:painting_id>/update', methods = ['POST'])    
def edit(painting_id):
    if Painting.validate_painting(request.form):
        data = {
            'id': painting_id,
            'title': request.form['title'],
            'description': request.form['description'],
            'price': request.form['price'],
            'users_id': session['user_id']
        }
        painting_id = Painting.edit_painting(data)
        print(painting_id)
    return redirect('/dashboard')
    # return redirect('/painting/<int:painting_id>/edit')


@app.route('/painting/<int:painting_id>/edit')
def edit_painting(painting_id):
    if 'user_id' not in session:
        flash('Log in to view this page')
        return redirect('/')
    data = {
        'id': painting_id
    }
    painting = Painting.get_painting(data)
    print(painting)
    return render_template('edit_painting.html', painting = painting)
    


@app.route('/painting/<int:painting_id>/delete')
def delete(painting_id):
    data = {
        'id': painting_id
    }
    Painting.delete(data)
    return redirect('/dashboard')

