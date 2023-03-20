from flask import Flask, render_template, request, redirect, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash
from flask_app.models.user_model import User

@app.route('/')
def index():
    return redirect('/users')


@app.route('/users')
def users():
    return render_template('login.html')


@app.route('/users/registration', methods=['POST'])
def registration():
    # check if passwords match
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/users')
    
    # create the hash
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_password)
    
    new_user = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_password
    }
    User.create_user(new_user)
    return redirect('/users')


@app.route('/users/login', methods=['POST'])
def login():
    get_email = {
        'email': request.form['email']
    }
    this_user = User.get_user_by_email(get_email)
    
    session['logged_in'] = True
    session['first_name'] = User.return_first_name(get_email)
    session['email'] = get_email['email']
    session['user_id'] = User.return_id(get_email)
    
    if not this_user:
        flash("Invalid email or password", "login")
        return redirect('/users')
    
    if not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash('Incorrect password', "login")
        return redirect('/users')

    return redirect('/recipes')
        
    
@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/users')
