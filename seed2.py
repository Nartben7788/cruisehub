# from app import db, app
from databases import db, app, User, Owner, Car, Reservations
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed_data():
    with app.app_context():
        car7 = Car(
            model='Corolla',
            make ='Toyota',
            price=300,
            additional_info='open to negotiation',
            picture='static/uploads/ethan_johnson/corolla.jpg',
            owner_id= 4)
            
        
        db.session.add(car7)
        db.session.commit()
       
        
        
        
        

       
        # # Add data to the database
        # db.session.add_all([car1, car2,car3,car4, car5, car6,])
        # db.session.commit()

if __name__ == "__main__":
    seed_data()
