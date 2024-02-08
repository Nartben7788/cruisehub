# from app import db, app
from databases import db, app, User, Owner, Car, Reservations
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed_data():
    with app.app_context():
        owner_data = [
            {
                'name': 'Casey Parker',
                'phone_number': '7034123859',
                'email': 'cassiep@gmail.com',
                'username': 'PCassie',
                'password':generate_password_hash('ownerpass5', method='pbkdf2:sha256'), 
                'user_type':'owner'
            },
            {
                'name': 'Anthonia Miller',
                'phone_number': '7034121259',
                'email': 'anthonymiller@gmail.com',
                'username': 'toni_mills',
                'password':generate_password_hash('ownerpass6', method='pbkdf2:sha256'), 
                'user_type':'owner'  
            },
            {   'name': 'Elena Day',
                'phone_number': '0341238579',
                'email': 'elenaday@gmail.com',
                'username': 'Elenay_day',
                'password':generate_password_hash('ownerpass7', method='pbkdf2:sha256'), 
                'user_type':'owner'
            },
            {
                'name': 'Wisdom Akan',
                'phone_number': '123423859',
                'email': 'akanwisdom@gmail.com',
                'username': 'Wisdom_a',
                'password':generate_password_hash('ownerpass8', method='pbkdf2:sha256'), 
                'user_type':'owner'
            },
            {
                'name': 'Temiloluwa Ajala',
                'phone_number': '7034123859',
                'email': 'tessie@gmail.com',
                'username': 'Tessie',
                'password':generate_password_hash('ownerpass9', method='pbkdf2:sha256'), 
                'user_type':'owner'
            },
            {
                'name': 'Precious King',
                'phone_number': '71123123859',
                'email': 'Kingprecious@gmail.com',
                'username': 'King_Precious',
                'password':generate_password_hash('ownerpass10', method='pbkdf2:sha256'), 
                'user_type':'owner'
            },
            {
                'name': 'Anthony Wade',
                'phone_number': '701134123859',
                'email': 'tonyWade@gmail.com',
                'username': 'tony_wade',
                'password':generate_password_hash('ownerpass4', method='pbkdf2:sha256'), 
                'user_type':'owner'
            }

           
           
            
            
             
        ]
        for data in owner_data:
            owner = Owner(**data)
            db.session.add(owner)
        db.session.commit()

if __name__ == "__main__":
    seed_data()
