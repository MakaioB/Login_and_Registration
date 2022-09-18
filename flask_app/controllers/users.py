from flask import Flask, render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#render_templates
@app.route('/')
def index():
    return render_template('home_page.html')

@app.route('/hello_page')
def display_dashboard():
    if not 'user_id' in session:
        flash("Must be logged in.")
        return redirect("/")
    return render_template('hello_page.html')

#register
@app.route('/register', methods=['POST'])
def register():
    # validate the form here ...
    if not User.validate_registration(request.form):
        #redirect to the form page
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'password_confirmation': request.form['password_confirmation']
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    print (user_id)
    session_data = {'id': user_id}
    get_user = User.get_by_id(session_data)
    # store user id into session
    session['user_id'] = get_user.first_name
    return redirect("/hello_page")

#login
@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['user_first_name'] = user_in_db.first_name
    # never render on a post!!!
    return redirect("/hello_page")

#session pop
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_first_name', None)
    return redirect('/')