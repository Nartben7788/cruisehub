from flask import render_template, request, redirect, url_for, flash, session
from flask_session import Session
from flask_mail import Mail, Message 
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
import secrets
from time import time
from databases import*

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'cruise.carhub@gmail.com'
app.config['MAIL_PASSWORD'] = 'dlfi gmyd vrfs enhm'
mail = Mail(app)

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
        elif user_type == "owner":
            user = Owner.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = user.user_type
            if user.user_type == 'user':
                return redirect(url_for('user_dashboard' ))
            else:
                return redirect(url_for('owner_dashboard', owner_id = user.id))
        else:
            flash('Incorrect username or password', 'login')
    else:
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user and 'user_type' in session and session['user_type'] == user.user_type:
                if user.user_type == 'user':
                    return redirect(url_for('user_dashboard'))
                elif user.user_type == 'owner':
                    return redirect(url_for('owner_dashboard', owner_id=user.id))

    return render_template('login.html')
@app.route('/logout')
def logout():
    # Remove owner_id from the session during logout 
    session.pop('user_id', None)
    session.pop('user_type', None)      
    return redirect(url_for('login'))

# Route for handling the car form submission
@app.route('/add_car', methods=['POST', 'GET'])
def add_car():
    if 'user_id' not in session:
        # Redirect to login if owner is not logged in
        return redirect(url_for('login'))

    owner_id = session['user_id']
    user = db.session.get(Owner, owner_id)
    # user = Owner.query.get(owner_id)

    if request.method == 'GET':
        return render_template('add_car.html', user=user)
    else:
        model = request.form['model']
        make = request.form['make']
        price = request.form['price']
        additional_info = request.form['additional_info']
        picture = save_picture(request.files['picture'], owner_id)

        # Validate the price field
        try:
            price = float(price)  # Convert price to a float
        except ValueError:
            # If the price cannot be converted to a float, return an error
            flash('Price must be a valid number', 'add')
            return redirect(url_for('add_car'))

        if price <= 0:
            flash('Price must be greater than zero', 'add')
            return redirect(url_for('add_car'))


        new_car = Car(
            model=model,
            make=make,
            price=price,
            picture=picture,
            additional_info=additional_info,
            owner_id=owner_id,
            status='available'
        )

        db.session.add(new_car)
        db.session.commit()

        return redirect(url_for('owner_dashboard', owner_id=owner_id))

def save_picture(picture, owner_id):
    owner = db.session.get(Owner, owner_id)
    # owner = Owner.query.get(owner_id)
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
       
        if user and 'user_type' in session and session['user_type'] == user.user_type:
          
            page = request.args.get('page', 1, type=int)
            per_page = 6  # Number of cars per page

            # Retrieve filtering criteria from the request
            make = request.args.get('make')
            model = request.args.get('model')
            price = request.args.get('price')

            # Query all cars to count total number of cars
            all_cars_query = Car.query

            if make:
                all_cars_query = all_cars_query.filter(Car.make.ilike(f'%{make}%'))
            if model:
                all_cars_query = all_cars_query.filter(Car.model.ilike(f'%{model}%'))
            if price:
                all_cars_query = all_cars_query.filter(Car.price <= float(price))

            total_cars_count = all_cars_query.count()

            # Paginate the filtered query
            filtered_cars = all_cars_query.paginate(page=page, per_page=per_page, error_out=False)

            return render_template('user_dashboard.html', filtered_cars=filtered_cars, user=user, total_cars_count=total_cars_count)
    else:
        return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/clear_filters', methods=['GET'])
def clear_filters():
    # Redirect back to the user dashboard without any filtering criteria
    return redirect(url_for('user_dashboard'))
        
@app.route('/car_profile/<int:car_id>')
def car_profile(car_id):
    car = Car.query.get_or_404(car_id)
    if 'user_id' in session:
        user_id = session['user_id']
        user_type = session['user_type']

        if user_type == 'user':
            user = User.query.get_or_404(user_id)
        elif user_type == 'owner':
            user = Owner.query.get_or_404(user_id)
        else:
            return redirect(url_for('login'))

        owner = Owner.query.get_or_404(car.owner_id)
        return render_template('car_profile.html', car=car, owner=owner, user=user)
    else:
        # Redirect to login if user is not logged in
        return redirect(url_for('login'))
    

@app.route('/owner_profile/<int:owner_id>')
def owner_profile(owner_id):
    owner = Owner.query.get_or_404(owner_id)
    cars = Car.query.filter_by(owner_id=owner_id).all()
    return render_template('owner_profile.html', owner=owner, cars=cars)

@app.route('/owner/<int:owner_id>')
def owner_dashboard(owner_id):
    if 'user_id' in session and owner_id ==  session['user_id']:
        owner = db.session.get(Owner, owner_id)
        # owner = Owner.query.get(owner_id)
        if session['user_type'] == owner.user_type:
            cars = Car.query.filter_by(owner_id=owner_id).all()
            return render_template('owner_dashboard.html',owner = owner, cars=cars)
        else:
            return redirect(url_for('login'))
    else :
        return redirect(url_for('login'))
    
@app.route('/owner/<int:owner_id>/update_status/<int:car_id>',methods=["POST"])
def update_status(owner_id,car_id):
    """Handle a request to cancel a car listing"""
    if 'user_id' in session and owner_id ==session['user_id']:
        car = Car.query.get_or_404(car_id)
        owner = Owner.query.get_or_404(car.owner_id)
        # reservations = Reservations.query.filter_by(reserved_car_id=car.id).all()

        if car.status == 'available':
            car.status = 'maintenance'  # Set status to 'maintenance' when canceling a car
            db.session.commit()

            msg = Message('Car Removed' ,sender= 'cruise.carhub@gmail.com', recipients= [owner.email])
            msg.body=f' Dear {owner.name}. This is confirming that you removed your car from the car marketplace.'
            mail.send(msg)
            
            flash("Car has been successfully removed from marketplace for maintenance", 'cancel_car')
            return redirect(url_for('owner_dashboard',owner_id=owner_id))
        elif car.status == 'maintenance':
            car.status = 'available'
            db.session.commit()

            msg = Message('Car Restored for Reservation' ,sender= 'cruise.carhub@gmail.com', recipients= [owner.email])
            msg.body=f' Dear {owner.name}. This is confirming that you have succesfully returned  your car for reservation.'
            mail.send(msg)
            
            flash("Car is now available for reservation", 'cancel_car')
            return redirect(url_for('owner_dashboard',owner_id=owner_id))

      
    else:
        return redirect(url_for(login))

@app.route('/owner/reservations/<int:owner_id>')
def show_reservation(owner_id):
    if 'user_id' in session and owner_id ==  session['user_id']:
        owner = Owner.query.get(session['user_id'])
        reservations = Reservations.query.filter_by(owner_id=owner_id).all()
        reserved_cars = []
        for reservation in reservations:
            car = Car.query.get(reservation.reserved_car_id)
            user = User.query.get(reservation.user_id)
            reserved_cars.append((reservation, car,user))
        return render_template("show_reservations.html", reservations=reservations, reserved_cars=reserved_cars, user=user, owner = owner) 
    return redirect(url_for('login'))

#An email should be sent to the owner when reservation is made

@app.route("/reservation/<int:car_id>", methods=['POST', 'GET'])
def reservation(car_id):
    
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect(url_for('login'))
        car = Car.query.get_or_404(car_id)
        user = User.query.get(session['user_id'])
        # Check if the car has existing reservations
        existing_reservations = Reservations.query.filter_by(reserved_car_id=car_id).all()

        if existing_reservations:
            # Find the latest end date of existing reservations
            latest_end_date = max(reservation.end_date for reservation in existing_reservations)

            # Set the earliest start date to 2 days after the latest end date
            earliest_start_date = latest_end_date + timedelta(days=2)
        else:
            # If no existing reservations, set the earliest start date to the current date
            earliest_start_date = datetime.now()
        
        return render_template('reservation.html', earliest_start_date=earliest_start_date.strftime('%Y-%m-%d'), car_id=car_id, car=car, user=user)
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
            owner = Owner.query.get(owner_id)
            user = User.query.get(user_id)
           

            
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
            
            reservation = new_reservation.id
            db.session.commit()
           
            user_msg = Message('Reservation Confirmation' ,sender= 'cruise.carhub@gmail.com', recipients= [user.email])
            user_msg.body=f' Dear {user.name}. This is confirming your reservation with the reservation ID : {reservation} \n from {start_date.strftime("%b %d, %Y")} to {end_date.strftime("%b %d, %Y")}'
            mail.send(user_msg)


            owner_msg = Message('New Reservation' ,sender= 'cruise.carhub@gmail.com', recipients= [owner.email])
            owner_msg.body=f' Dear {owner.name}. \n Your car {car.make} {car.model} ID : {car.id} has been reserved by {user.name} with the reservation ID : {reservation} from \n {start_date.strftime("%b %d, %Y")} to {end_date.strftime("%b %d, %Y")}'
            mail.send(owner_msg)
           
            

           
            return redirect(url_for('user_dashboard'))
            

@app.route('/my_reservations', methods =["GET"])
def user_reservations():
    """Returns all of the user's past and future reservations"""
    if 'user_id' not in session:
        return redirect(url_for("login"))
    else:   
        user_id = session['user_id']
        reservations = Reservations.query.filter_by(user_id=user_id).all()
        reserved_cars = []
        for reservation in reservations:
            car = Car.query.get(reservation.reserved_car_id)
            reserved_cars.append((reservation, car))
        return render_template('user_reservations.html', reserved_cars = reserved_cars, reservations = reservations)


@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    if 'user_id' in session:
        user = User.query.get_or_404(session['user_id'])
        reservation = Reservations.query.get_or_404(reservation_id)
        start_date = reservation.start_date
        end_date = reservation.end_date
        owner = Owner.query.get_or_404(reservation.owner_id)
        car = Car.query.get_or_404(reservation.reserved_car_id)

        db.session.delete(reservation)
        user_msg = Message('Reservation Cancelled' ,sender= 'cruise.carhub@gmail.com', recipients= [user.email])
        user_msg.body=f' Dear {user.name}. This is confirming you cancelled your reservation with the reservation ID :{reservation_id} \n from {start_date.strftime("%b %d, %Y")} to {end_date.strftime("%b %d, %Y")}'
        mail.send(user_msg)

        owner_msg = Message('Reservation Cancelled' ,sender= 'cruise.carhub@gmail.com', recipients=[owner.email])
        owner_msg.body=f' Dear {owner.name}. \n The reservation for your car {car.make} {car.model} with \n Car ID : {car.id} has been cancelled'
        mail.send(owner_msg)
            
        db.session.commit()
        return redirect(url_for('user_reservations'))
    else:
        return redirect(url_for('login'))

@app.route('/owner/<int:owner_id>/remove/<int:car_id>',methods=["POST"]) 
def remove_car(owner_id, car_id):
    """Handle a request to cancel a car listing"""
    if 'user_id' in session and owner_id ==session['user_id']:
        car = Car.query.get_or_404(car_id)
        owner = Owner.query.get_or_404(car.owner_id)
        
        reservations = Reservations.query.filter_by(reserved_car_id=car.id).all()
        if not reservations:
            db.session.delete(car)
            msg = Message('Car Removed' ,sender= 'cruise.carhub@gmail.com', recipients= [owner.email])
            msg.body=f' Dear {Owner.name}. This is confirming that you removed your car from the car marketplace.'
            mail.send(msg)
            db.session.commit()
            flash("Car has been successfully removed from marketplace", 'remove_car')
            return redirect(url_for('owner_dashboard',owner_id=owner_id))
        else:
            msg = Message('Car Removed' ,sender= 'cruise.carhub@gmail.com', recipients= [owner.email])
            msg.body=f' Dear {Owner.name}. This is confirming that you removed your car from the car marketplace.'
            mail.send(msg)
            flash("Car cannot be removed from marketplace because it has been reserved", 'remove_car')

    return redirect(url_for('login'))

@app.route('/forgot_password', methods = ['POST', 'GET'])
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/submit_token', methods=['GET', 'POST'])
def submit_token():

    if request.method == 'POST':
        email = request.form['email']

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Invalid email!")
            return render_template("submit_token.html")
            
        elif user:
            random_number = secrets.randbelow(1000000)

            token = '{:06d}'.format(random_number)
            user.reset_token = token
            user.reset_token_timestamp = datetime.utcnow()
            db.session.commit()

            user_message = Message("Password Reset Request", sender="cruise.carhub@gmail.com", recipients= [user.email])
            user_message.body = f'''To reset your password, visit the following link:
                {url_for('submit_token', _external =True)} and enter this token [{user.reset_token}]
                If you did not make this request then simply ignore this email and no changes will be made.
                '''
            mail.send(user_message)
            flash("An email has been sent to you with a reset token")
            return render_template("submit_token.html", email = email)
        

        
        owner = Owner.query.filter_by(email=email).first()
        if not owner:
            flash("invalid email!")
            return render_template("submit_token.html")

        elif owner:
            random_number = secrets.randbelow(1000000)
            token = '{:06d}'.format(random_number)
            owner.reset_token = token
            owner.reset_token_timestamp = datetime.utcnow()
            db.session.commit()

            owner_message = Message("Password Reset Request", sender="cruise.carhub@gmail.com", recipients= [owner.email])
            owner_message.body = f'''To reset your password, visit the following link: 
                                {url_for('submit_token', _external=True)}  and enter this token [{owner.reset_token}]
                    If you did not make this request then simply ignore this email and no changes will be made.

                    '''
            mail.send(owner_message)
            flash("An email has been sent to you with a reset token")
        
            return render_template("submit_token.html")

    return render_template('submit_token.html')



@app.route('/reset_password', methods=['POST'])
def reset_password():

    if request.method == 'POST':
        token = request.form["token"]
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        user_type = request.form['user_type']
        email = request.form["email"]

        if user_type == "user":
            user = User.query.filter_by(reset_token=token, email=email).first()
            
            if user and user.email:
                if token == str(user.reset_token):
                    if user.reset_token and (user.reset_token_timestamp) < (datetime.utcnow() + timedelta(minutes=10)):
                        
                        error_messages = []

                        has_uppercase = False
                        has_lowercase = False
                        has_symbol = False

                        if len(new_password) < 6:
                            error_messages.append("Password must have at least 6 characters." )

                        else:
                            for char in new_password:
                                if char.isupper():
                                    has_uppercase = True
                                elif char.islower():
                                    has_lowercase = True
                                elif char in "!@#$%^&*.()_+{}|<>?~-":
                                    has_symbol = True
                        
                        if not has_uppercase:
                            error_messages.append("Password must contain at least one uppercase letter." )
                        if not has_lowercase:
                            error_messages.append("Password must contain at least one lowercase letter.")
                        if not has_symbol:
                            error_messages.append("Password must contain at least one symbol.")

                        if error_messages:
                            flash(".".join(error_messages), "danger")
                            return render_template("submit_token.html",messages=error_messages, email=email)


                        if new_password == confirm_password:
                            
                            user.password = generate_password_hash(new_password)
                            user.reset_token = None
                            db.session.commit()

                            flash('Password reset successful. You can now log in with your new password.')
                            return redirect(url_for('login'))
                        
                        else:
                            flash('Passwords do not match!')
                            return redirect(url_for('submit_token'))  
                    else:
                        flash("Invalid or expired token!" )
                        return redirect(url_for('forgot_password')) 
                else:
                        flash("Invalid or expired token!" )
                        return redirect(url_for('forgot_password')) 
            else:
                return redirect(url_for("signup"))
        
        elif user_type == "owner":
            owner = Owner.query.filter_by(reset_token=token, email= email).first()

            if owner and owner.email:
                if token == str(owner.reset_token):
                    if owner.reset_token and (owner.reset_token_timestamp) < (datetime.utcnow() + timedelta(minutes=10)):

                        error_messages = []

                        has_uppercase = False
                        has_lowercase = False
                        has_symbol = False

                        if len(new_password) < 6:
                            error_messages.append("Password must have at least 6 characters.",)

                        else:
                            for char in new_password:
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
                            flash(".".join(error_messages), "token")
                            return render_template("submit_token.html", messages=error_messages, email=email)

                        if new_password == confirm_password:

                            owner.password = generate_password_hash(new_password)
                            owner.reset_token = None
                            db.session.commit()

                            flash('Password reset successful. You can now log in with your new password.')
                            return redirect(url_for('login'))
                        
                        else:
                            flash('Passwords do not match!')
                            return redirect(url_for('submit_token'))  
                        
                    else:
                        flash("Invalid or expired token!")
                        return redirect(url_for('forgot_password'))
                else:
                    flash("Invalid or expired token!")
                    return redirect(url_for('forgot_password')) 
            else:
                return redirect(url_for('signup'))


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

           
#         except Exception as e:
#             # Handle exceptions if any
#             print('hello')

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