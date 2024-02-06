from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta

from databases import*



@app.route("/")
def home():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']  

        #validate Phone Number
        if len(phone_number)<10:
            flash('Phone Number must be at leastr 10 Digits long.','error')
            return redirect(url_for('signup'))
          # Validate password conditions
        error_messages = []

        # Flag variables to track if conditions are met
        has_uppercase = False
        has_lowercase = False
        has_symbol = False

        if len(password) < 6:
            error_messages.append("Password must have at least 6 characters.")
        else:
            for char in password:
                if char.isupper():
                    has_uppercase = True
                elif char.islower():
                    has_lowercase = True
                elif char in "!@#$%^&*.()_+{}|<>?~-":
                    has_symbol = True

        if not has_uppercase:
            error_messages.append("Password must contain at least one uppercase letter.")
        if not has_lowercase:
            error_messages.append("Password must contain at least one lowercase letter.")
        if not has_symbol:
            error_messages.append("Password must contain at least one symbol.")

        if error_messages:
            # If there are error messages, flash them and redirect back to signup
            flash(". ".join(error_messages), "error")
            return redirect(url_for('signup'))



        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if user_type == 'user':
            new_user = User(
                name=name, 
                phone_number=phone_number, 
                email=email,
                username=username, 
                password=hashed_password)
            new_user_or_owner = new_user
        elif user_type == 'owner':
            new_owner = Owner(
                name=name,
                phone_number=phone_number, 
                email=email, 
                username=username, 
                password=hashed_password)
            new_user_or_owner = new_owner
        try:
            # Try to add the new user or owner to the database
            db.session.add(new_user_or_owner)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError as e: 
            db.session.rollback()
            if "UNIQUE constraint failed: user.email" in str(e) or "UNIQUE constraint failed: owner.email" in str(e):
                flash("Email already exists. Please choose a different one.", "error")
            elif "UNIQUE constraint failed: user.username" in str(e) or "UNIQUE constraint failed: owner.username" in str(e):
                flash("Username already exists. Please choose a different one.", "error")
            else:
                flash("Email or username already exists. Please choose a different one.", "error")

    return render_template('signup.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        if user_type == "user":
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('user_dashboard'))

            else:
                flash ("Invalid Username or Password!", 'login')
            
        elif user_type == "owner":
            owner = Owner.query.filter_by(username=username).first()
            if owner and check_password_hash(owner.password, password):
                session['owner_id'] = owner.id
                return redirect(url_for('add_car'))
            else:
                return render_template('login.html', error = 'Invalid username or password')
        else:
            flash ("You must choose your Account Type")
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove owner_id from the session during logout 
    session.pop('user_id', None)
    session.pop('owner_id', None)
    return redirect(url_for('login'))


# Route for handling the car form submission
@app.route('/add_car', methods=['POST', 'GET'])
def add_car():
    if request.method == 'GET':
        return render_template('owner.html')
    else:
        if 'owner_id' not in session:
        # Redirect to login if owner is not logged in
            return redirect(url_for('login'))

        owner_id = session['owner_id']
        model = request.form['model']
        make = request.form['make']
        year = request.form['year']
        price = request.form['price']
        additional_info = request.form['additional_info']
        picture = save_picture(request.files['picture'],owner_id)

        new_car = Car(
            model=model, 
            make=make, 
            year=year, 
            price=price,
            picture=picture, 
            additional_info=additional_info,
            owner_id=owner_id)

        db.session.add(new_car)
        db.session.commit()

        return redirect(url_for('home'))

def save_picture(picture, owner_id):
    owner = Owner.query.get(owner_id)
    owner_username = owner.username
    uploads_folder = os.path.join('static', 'uploads', owner_username)
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder) 
    picture_filename = secure_filename(picture.filename)
    picture_path = os.path.join(uploads_folder, picture_filename)
    picture.save(picture_path)
    return picture_path

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            page = request.args.get('page', 1, type=int)
            per_page = 6

              # Retrieve filtering criteria from the request
            make = request.args.get('make')
            model = request.args.get('model')
            price = request.args.get('price')

            # Query cars based on filtering criteria
            filtered_cars_query = Car.query

            if make:
                filtered_cars_query = filtered_cars_query.filter(Car.make.ilike(f'%{make}%'))
            if model:
                filtered_cars_query = filtered_cars_query.filter(Car.model.ilike(f'%{model}%'))
            if price:
                filtered_cars_query = filtered_cars_query.filter(Car.price <= float(price))

            # cars = Car.query.paginate(page=page, per_page=per_page, error_out=False)
            # return render_template('user_dashboard.html', cars=cars, user=user)
            # Paginate the filtered query
            filtered_cars = filtered_cars_query.paginate(page=page, per_page=per_page, error_out=False)
            return render_template('user_dashboard.html', filtered_cars=filtered_cars, user=user)
    return redirect(url_for('login'))
        
@app.route('/car_profile/<int:car_id>')
def car_profile(car_id):
    car = Car.query.get_or_404(car_id)
    owner = Owner.query.get_or_404(car.owner_id)
    return render_template('car_profile.html', car=car, owner=owner)
    

@app.route('/owner/<int:owner_id>')
def owner_profile(owner_id):
    owner = Owner.query.get_or_404(owner_id)
    cars = Car.query.filter_by(owner_id=owner_id).all()
    return render_template('owner_profile.html', owner=owner, cars=cars)

@app.route("/reservation/<int:car_id>", methods=['POST', 'GET'])
def reservation(car_id):
    
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect(url_for('login'))
        # Check if the car has existing reservations
        existing_reservations = Reservations.query.filter_by(reserved_car_id=car_id).all()

        if existing_reservations:
            # Find the latest end date of existing reservations
            latest_end_date = max(reservation.end_date for reservation in existing_reservations)

            # Set the earliest start date to the day after the latest end date
            earliest_start_date = latest_end_date + timedelta(days=1)
        else:
            # If no existing reservations, set the earliest start date to the current date
            earliest_start_date = datetime.now()
        
        return render_template('reservation.html', earliest_start_date=earliest_start_date.strftime('%Y-%m-%d'), car_id=car_id)
    else:
        if 'user_id' not in session:    
            return redirect(url_for('login'))
        
        else:
            start_date_str = request.form['start_date']
            end_date_str = request.form['end_date']
            user_id = session['user_id']  # Access user_id directly from session
            car = Car.query.get(car_id)
            reserved_car_id = car_id
            owner_id = car.owner_id

            
            # Convert string dates to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            new_reservation = Reservations(
                start_date=start_date,
                end_date=end_date,
                reserved_car_id=reserved_car_id,
                user_id=user_id,
                owner_id=owner_id  
            )
            db.session.add(new_reservation)
            db.session.commit()

            flash('Reservation completed successfully!', 'success')
            return redirect(url_for('home'))



# @app.route('/delete_all_entries', methods=['GET', 'POST'])
# def delete_all_entries():
#     if request.method == 'GET':
#         try:
#             # Delete all entries in the User table
#             db.session.query(Car).delete()

#             # Delete all entries in the Owner table
#             db.session.query(User).delete()
#             db.session.query(Reservations).delete()
#             db.session.query(Owner).delete()

#             # # Commit the changes to the database
#             db.session.commit()

#            
#         except Exception as e:
#             # Handle exceptions if any
#             

#         return redirect(url_for('home'))  # Redirect to the home page or any other page

#     return render_template('delete_entries.html')  # Create a template for the delete_entries page
        
# @app.route('/delete_tables', methods=['GET', 'POST'])
# def delete_tables():
#     if request.method == 'GET':
#         try:
#             # Delete the User table
           

#             # Delete the Owner table
            
#             Car.__table__.drop(db.engine)
#             Reservations.__table__.drop(db.engine)

#             flash('Tables deleted successfully!')
#         except Exception as e:
#             # Handle exceptions if any
#             flash(f'Error deleting tables: {str(e)}', 'delete')

#         return redirect(url_for('home'))  # Redirect to the home page or any other page

#     return render_template('delete_entries.html')  # Create 
if __name__ == "__main__":
    app.run(debug=True)