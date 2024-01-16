
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

if __name__ == "__main__":
    app.run(debug=True)