from app import db, User, Owner, Car, Reservations
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed_data():
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

    # Create sample cars
    car1 = Car(
        model='Toyota Camry',
        make='Toyota',
        year=2022,
        price=25000,
        additional_info='Sleek and fuel-efficient',
        picture='static/toyota_camry.jpg',
        owner_id=1
    )

    car2 = Car(
        model='Honda Civic',
        make='Honda',
        year=2023,
        price=22000,
        additional_info='Compact and reliable',
        picture='static/honda_civic.jpg',
        owner_id=2
    )

    car3 = Car(
        model='Honda Civic',
        make='Honda',
        year=2023,
        price=22000,
        additional_info='Compact and reliable',
        picture='static/honda_civic.jpg',
        owner_id=1
    )

    # Create sample reservations
    reservation1 = Reservations(
        start_date=datetime(2022, 3, 1),
        end_date=datetime(2022, 3, 10),
        user_id=1,
        reserved_car_id=1
    )

    reservation2 = Reservations(
        start_date=datetime(2023, 4, 15),
        end_date=datetime(2023, 4, 25),
        user_id=2,
        reserved_car_id=2
    )

    # Add data to the database
    db.session.add_all([user1, user2, owner1, owner2, car1, car2,car3, reservation1, reservation2])
    db.session.commit()

if __name__ == "__main__":
    seed_data()
