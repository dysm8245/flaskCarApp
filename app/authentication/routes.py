from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from forms import UserSignupForm, UserLoginForm
from models import User, db, check_password_hash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            first_name = request.json['first']
            last_name = request.json['last']
            email = request.json['email']
            username = request.json['username']
            password = request.json['password']

            user = User(first_name, last_name, email, username, password)

            db.session.add(user)
            db.session.commit()

            print('successfully added user')
            
            return jsonify({
                "token": user.token
            })
        else:
            return jsonify({
                "error": "Couldn't create account"
            }, 401)
    except:
        raise Exception('Invalid form data: Please check your form')
    
    # return render_template('signup.html')

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        if request.method == 'POST':
            username = request.json["username"]
            password = request.json["password"]

            logged_user = User.query.filter(User.username == username).first()
            if logged_user and check_password_hash(logged_user.password, password):
                # login_user(logged_user)
                # print('logged in')
                return jsonify({
                    "token": logged_user.token
                }) 
            else:
                return jsonify({
                    "error": "No user in Database"
                }, 401)
    except:
        raise Exception('Invalid form data: Please check your form')
    
    # return render_template('signin.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))
