from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_bcrypt import Bcrypt 

from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Log in to view this page')
        return redirect('/')

    return render_template('dashboard.html', recipes = Recipe.get_all_recipes())

@app.route('/create/recipe')
def create_recipe():
    if 'user_id' not in session:
        flash('Log in to view this page')
        return redirect('/')
    return render_template('create_recipe.html')


@app.route('/new/recipe', methods=['POST'])
def new_recipe():
    data = {
        'name': request.form['name'],
        'date': request.form['date'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'timing': request.form['timing'],
        'users_id': session['user_id']
    }
    recipe_id = Recipe.new_recipe(data)
    print(recipe_id)

    return redirect('/dashboard')

@app.route('/recipes/<int:recipe_id>')
def get_recipe(recipe_id):
    data ={
        'id': recipe_id
    }
    recipes = Recipe.get_recipe(data)
    return render_template('show_recipe.html', recipes = recipes)

@app.route('/recipes/<int:recipe_id>/update', methods = ['POST'])    
def edit(recipe_id):
    data = {
        'id': recipe_id,
        'name': request.form['name'],
        'date': request.form['date'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'timing': request.form['timing'],
        # 'users_id': session['user_id']
    }
    Recipe.edit_recipe(data)
    print(recipe_id)
    return redirect(f'/recipes/{recipe_id}')

@app.route('/recipe/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    recipes = Recipe.get_recipe(data)
    print(recipes)
    return render_template('edit_recipe.html', recipes = recipes)
    


@app.route('/recipe/<int:recipe_id>/delete')
def delete(recipe_id):
    data = {
        'id': recipe_id
    }
    Recipe.delete(data)
    return redirect('/dashboard')

