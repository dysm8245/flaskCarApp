from flask import Blueprint, render_template, request, redirect, url_for, flash
from forms import UserSignupForm, UserLoginForm
from models import User, db, check_password_hash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignupForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data

            user = User(first_name, last_name, email, username, password)

            db.session.add(user)
            db.session.commit()

            print('successfully added user')
            
            return redirect(url_for('site.profile'))
        else:
            print("couldn't add user")
    except:
        raise Exception('Invalid form data: Please check your form')
    
    return render_template('signup.html', form = form)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            print('valid')
            username = form.username.data
            password = form.password.data

            logged_user = User.query.filter(User.username == username).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                print('logged in')
                return redirect(url_for('site.profile'))
            else:
                print('We were not able to log in this user')
    except:
        raise Exception('Invalid form data: Please check your form')
    
    return render_template('signin.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))
