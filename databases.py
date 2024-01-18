
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cruisehub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yWNZU7s8'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
 


with app.app_context():
    db.create_all()

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_type = db.Column(db.String, nullable=False, default='user')

#Define the Owner model
class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_type = db.Column(db.String, nullable=False, default='owner') 

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=False)
    make = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    additional_info = db.Column(db.String, nullable=False)
    picture = db.Column(db.String)  # You might want to store the file path or use a proper file storage solution
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)


class Reservations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reserved_car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    user = db.relationship('User', backref='reservations')
    reserved_car = db.relationship('Car', backref='reservations')



car_info = {
            'model':'Ask wiki',
            'make':'Rolls Royce',
            'year':2024,
            'price':5000,
            'additional_info':'Beautiful and fast',
            'picture':'static/images.jpg',
            'owner_id': 3}

new_car = Car(**car_info)
db.session.add(new_car)
db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)