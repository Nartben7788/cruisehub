
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cruisehub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yWNZU7s8'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'cruisehub'
app.config['MAIL_PASSWORD'] = '[Yet to Come!]'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

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
    price = db.Column(db.Integer, nullable=False)
    additional_info = db.Column(db.String, nullable=False)
    picture = db.Column(db.String)  
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)


class Reservations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable= False)
    reserved_car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable = False)
    

    def cancel_reservation(self):
        if self.start_date > datetime.now():
            self.status = 'canceled'  
            db.session.commit()

            owner = Owner.query.get(self.owner_id) 
            owner_email = owner.email
            msg = Message('Reservation Cancellation', sender='cruisehub@gmail.com', recipients=[owner_email])
            msg.body = f'Hello, the reservation for your car {self.reserved_car.name} has been canceled.'
            mail.send(msg)
            
            return True  
        else:
            return False 
   
    






if __name__ == "__main__":
    app.run(debug=True)