# from app import db, app
from databases import db, app, User, Owner, Car, Reservations
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed_data():
    with app.app_context():
        car_data = [
            {
                'model': 'Corolla',
                'make': 'Toyota',
                'price': 300,
                'additional_info': 'open to negotiation',
                'picture': 'static/uploads/ethan_johnson/corolla.jpg',
                'owner_id': 4
            },
           
            {
                'model': 'A4',
                'make': 'Audi',
                'price': 800,
                'additional_info': 'fast on the road',
                'picture': 'static/uploads/benny_johnson/audi.jpg',
                'owner_id': 6
            },
            {
                'model': 'Sonata',
                'make': 'Hyundai',
                'price': 600,
                'additional_info': 'affordable electric car',
                'picture': 'static/uploads/helena_smith/hyundai.jpg',
                'owner_id': 7
            },
            {
                'model': 'Benz',
                'make': 'Mercedes',
                'price': 400,
                'additional_info': 'Can roll!',
                'picture': 'static/uploads/jackson_wilson/mercedes.jpg',
                'owner_id': 8
            },
            {
                'model': 'Outback',
                'make': 'Subaru',
                'price': 700,
                'additional_info': 'sport car',
                'picture': 'static/uploads/nimi/subaru.jpg',
                'owner_id': 9
            },
            {
                'model': 'XC90',
                'make': 'Volvo',
                'price': 300,
                'additional_info': 'compact car',
                'picture': 'static/uploads/benny_johnson/volvo.jpg',
                'owner_id': 10
            },
            {
                'model': '7',
                'make': 'BMW',
                'price': 400,
                'additional_info': 'comfortable car',
                'picture': 'static/uploads/ethan_johnson/bmw7.jpg',
                'owner_id': 4
            },
            {
                'model': 'Wrangler',
                'make': 'Jeep',
                'price': 500,
                'additional_info': 'Strong',
                'picture': 'static/uploads/helena_smith/jeep.jpg',
                'owner_id': 5
            },
            {
                'model': 'Sorento',
                'make': 'Kia',
                'price': 300,
                'additional_info': 'compact car',
                'picture': 'static/uploads/jackson_wilson/sorento.jpg',
                'owner_id': 6
            },
            {
                'model': 'Model S',
                'make': 'Tesla',
                'price': 600,
                'additional_info': 'premium compact electric car',
                'picture': 'static/uploads/nimi/tesla.jpg',
                'owner_id': 7
            },
            {
                'model': 'Altima',
                'make': 'Nissan',
                'price': 700,
                'additional_info': 'premium compact SUV',
                'picture': 'static/uploads/benny_johnson/nissan.jpg',
                'owner_id': 8
            },
            {
                'model': '488',
                'make': 'Ferrari',
                'price': 500,
                'additional_info': 'in excellent condition',
                'picture': 'static/uploads/ethan_johnson/ferrari.jpg',
                'owner_id': 5
            },
            {
                'model': 'Challenger',
                'make': 'Dodge',
                'price': 400,
                'additional_info': 'well maintained',
                'picture': 'static/uploads/helena_smith/dodge.jpg',
                'owner_id': 6
            }
        ]
        for data in car_data:
            car = Car(**data)
            db.session.add(car)
        db.session.commit()

if __name__ == "__main__":
    seed_data()
