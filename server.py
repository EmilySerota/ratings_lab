"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')


@app.route('/users')
def user_list():
    """show list of users"""

    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/<user_id>')
def user_detail(user_id):

    user = User.query.get(user_id)
    return render_template('user_info.html', user=user)

@app.route('/register', methods=['GET'])
def register_form():
    """show registration form"""

    return render_template('register_form.html')


@app.route('/register', methods=['POST'])
def register_process():
    """process registration form"""

    email = request.form.get('email')
    password = request.form.get('password')

    # if email not in db, add them to db

    if not User.query.filter_by(email = email).all():
        print(User.query.filter_by(email = email).all())
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    return redirect('/')


@app.route('/login')
def login_form():
    """show login form"""

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login_process():
    """process login form"""

    #get email & password that user entered for comparison below
    email = request.form.get('email')
    password = request.form.get('password')
    #pull in information for that specific user by their email and place info to refer back to in variable user
    user = User.query.filter_by(email = email).first()

    # If user doesn't exist after searching by email above in db, bring them to register page
    if not user:
        return redirect('/register')
    #if the password user entered is not = to the password pulled in from that user variable above redirect    
    elif password != user.password:
        flash("Incorrect password")
        return redirect('/login')
    # otherwise if successful login, redirect to specific user page by sending to the route above with the id of that user variable info. 
    else:
        session['username'] = email
        return redirect(f"/users/{user.user_id}")


@app.route('/logout')
def logout():
    """process logout"""
    session.pop('username',None)
    flash("You are now logged out")
    return redirect('/')

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
