from databases import app, Car, db

# Define the context of the Flask application
with app.app_context():
    # Get all cars where status is NULL
    null_status_cars = Car.query.filter(Car.status == None).all()

    # Update the status of each car to 'available'
    for car in null_status_cars:
        car.status = 'available'

    # Commit the changes to the database
    db.session.commit()