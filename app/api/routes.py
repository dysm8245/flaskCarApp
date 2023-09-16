from flask import Blueprint, request, jsonify, render_template, flash, url_for, redirect
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
from helpers import token_required
from models import db, User, CarCollection
from forms import CarCreationForm
from models import car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api', template_folder='api_templates')

@api.route('/createCar', methods = ['GET', 'POST'])
def create_car():
    form = CarCreationForm()
    make = form.make.data
    model = form.model.data
    year = form.year.data
    user_token = form.user_token.data
    try:
        logged_user = User.query.get(user_token).first()
        if logged_user and request.method == 'POST' and form.validate_on_submit():
            car = CarCollection(make, model, year, user_token)

            db.session.add(car)
            db.session.commit()

            print('Car has been added to the database.')
            return redirect(url_for('site.profile'))
        else:
            print('We were not able to add your car to the database.')
    except:
        raise Exception('Invalid form data')

    return render_template('carCreation.html', form=form)

@api.route('/showCars', methods=['GET'])
def showCars():
    user_token = current_user.token
    cars = CarCollection.query.filter_by(user_token = user_token).all()

    response = cars_schema.dump(cars)
    return render_template('carTable.html', data=response)

@api.route('/create', methods=['POST'])
@token_required
def create(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    car = CarCollection(make, model, year, current_user_token.token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/getCars', methods=['GET'])
@token_required
def getCars(current_user_token):
    a_user = current_user_token.token
    cars = CarCollection.query.filter_by(user_token=a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/getCar/<id>', methods=['GET'])
@token_required
def getCar(current_user_token, id):
    car = CarCollection.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/updateCar/<id>', methods=['PUT'])
@token_required
def updateCar(current_user_token, id):
    car = CarCollection.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.user_token = request.json['user_token'] 

    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)


@api.route('/deleteCar/<id>', methods=['DELETE'])
@token_required
def deleteCar(current_user_token, id):
    car = CarCollection.query.get(id)

    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)
