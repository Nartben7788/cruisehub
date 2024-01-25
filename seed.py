# from app import db, app
from databases import db, app, User, Owner, Car, Reservations
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed_data():
    with app.app_context():
        
        # Create sample users
        user1 = User(
            name='Ife Williams',
            phone_number='1234567890',
            email='ifewilliams@outlook.com',
            username='ify_will',
            password=generate_password_hash('password123', method='pbkdf2:sha256'),
            user_type='user'
        )

        user2 = User(
            name='Sydney Nartey',
            phone_number='9876543210',
            email='sydtey@yahoo.com',
            username='sydney111',
            password=generate_password_hash('password456', method='pbkdf2:sha256'),
            user_type='user'
        )

        user3 = User(
            name='Daniel Brown', 
            phone_number='5554445566', 
            email='daniel@example.com', 
            username='daniel_brown', 
            password=generate_password_hash('passabc', method='pbkdf2:sha256'), 
            user_type='user'
        )

        # Create sample owners
        owner1 = Owner(
            name='Benjamin Johnson',
            phone_number='1112223333',
            email='johnson@gmail.com',
            username='benny_johnson',
            password=generate_password_hash('ownerpass1', method='pbkdf2:sha256'),
            user_type='owner'
        )

        owner2 = Owner(
            name='Helena Smith',
            phone_number='4445556666',
            email='helena_smith@example.com',
            username='helena_smith',
            password=generate_password_hash('ownerpass2', method='pbkdf2:sha256'),
            user_type='owner'
        )
        owner3 = Owner(
            name='Jackson Wilson', 
            phone_number='5554445566', 
            email='jackson@example.com',
            username='jackson_wilson', 
            password=generate_password_hash('ownerpass4', method='pbkdf2:sha256'), 
            user_type='owner')
        
        owner4 = Owner(
            name='Ethan Johnson', 
            phone_number='5552223344', 
            email='ethan@example.com', 
            username='ethan_johnson', 
            password=generate_password_hash('ownerpass2', method='pbkdf2:sha256'), 
            user_type='owner'
        )
        # Create sample cars
        car1 = Car(
            model='Toyota Camry',
            make='Toyota',
            year=2022,
            price=25000,
            additional_info='Sleek and fuel-efficient',
            picture='static/uploads/toyota_camry.jpg',
            owner_id=1
        )

        car2 = Car(
            model='Honda Civic',
            make='Honda',
            year=2023,
            price=22000,
            additional_info='Compact and reliable',
            picture='static/uploads/honda_civic.jpg',
            owner_id=2
        )

        car3 = Car(
            model='Honda Civic',
            make='Honda',
            year=2023,
            price=22000,
            additional_info='Compact and reliable',
            picture='static/uploads/honda_civic.jpg',
            owner_id=1
        )
        car4 = Car(
            model='Chevrolet Malibu', 
            make='Chevrolet', 
            year=2022, 
            price=27000, 
            additional_info='Modern design, spacious', 
            picture='static/uploads/car4.jpg', 
            owner_id=4
            )
        
        car5 = Car(
            model='Ford Mustang', 
            make='Ford', 
            year=2022, 
            price=35000, 
            additional_info='Powerful and sporty', 
            picture='static/uploads/car3.jpg', 
            owner_id=3
        )
        car6 = Car(
            model='Honda Accord', 
            make='Honda', 
            year=2022, 
            price=28000, 
            additional_info='Comfortable and stylish', 
            picture='static/uploads/car2.jpg', 
            owner_id=2
            )
        

        # Create sample reservations
        reservation1 = Reservations(
            start_date=datetime(2024, 3, 1),
            end_date=datetime(2024, 3, 10),
            user_id=1,
            reserved_car_id=1
        )

        reservation2 = Reservations(
            start_date=datetime(2024, 4, 15),
            end_date=datetime(2024, 4, 25),
            user_id=2,
            reserved_car_id=2
        )
        
        reservation3 = Reservations(
            start_date=datetime(2024, 5, 5),
            end_date=datetime(2024, 5, 15), 
            user_id=3, 
            reserved_car_id=6)

        # Add data to the database
        db.session.add_all([user1, user2 ,user3, owner1, owner2,owner3,owner4,car1, car2,car3,car4, car5, car6,  reservation1, reservation2, reservation3])
        db.session.commit()

if __name__ == "__main__":
    seed_data()
