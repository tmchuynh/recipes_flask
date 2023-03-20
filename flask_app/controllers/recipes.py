from flask import Flask, render_template, request, redirect, session
from flask_app import app
from flask import flash
from datetime import datetime

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.recipe_model import Recipe

@app.route('/recipes')
def view_recipes():
    list_of_recipes = Recipe.get_all_recipes()
    return render_template('view_recipes.html', list_of_recipes=list_of_recipes)

@app.route('/recipes/create')
def create_recipe():
    return render_template('add_recipe.html')

@app.route('/recipes/add', methods=['POST'])
def add_recipe():
    print("request form", request.form)

    if not Recipe.validate_recipe(request.form):
        flash('Invalid Recipe')
        return redirect('/recipes')
    

    date = datetime.strptime(str(request.form['date_made']), '%m/%d/%Y')

    if (request.form.get('if_under_30') == '1'):
        new_recipe = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_made': date.strftime('%Y-%m-%d'),
            'if_under_30': 1,
            'user_id' : session['user_id']
        }
    else:
        new_recipe = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_made': date.strftime('%Y-%m-%d'),
            'if_under_30': 0,
            'user_id' : session['user_id']
        }

    Recipe.create_recipe(new_recipe)
    return redirect('/recipes')

@app.route('/recipes/details/<int:recipe_id>')
def view_recipe(recipe_id):
    this_recipe = {
        'id': recipe_id
    }
    print(this_recipe)
    recipe = Recipe.get_recipe_by_id(this_recipe)
    user = Recipe.get_user_created(this_recipe)
    return render_template('recipe_details.html', recipe=recipe, user=user)

@app.route('/recipes/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    this_recipe = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(this_recipe)
    
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    this_recipe = {
        'id': recipe_id
    }
    Recipe.delete_recipe(this_recipe)
    return redirect('/recipes')