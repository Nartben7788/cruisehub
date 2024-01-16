from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


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

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if user_type == 'user':
            new_user = User(
                name=name, 
                phone_number=phone_number, 
                email=email,
                username=username, 
                password=hashed_password)
            db.session.add(new_user)
        elif user_type == 'owner':
            new_owner = Owner(
                name=name, 
                phone_number=phone_number, 
                username=username, 
                email=email, 
                password=hashed_password)
            db.session.add(new_owner)

        db.session.commit()

        return redirect(url_for('home'))

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
                return "Login Successfull!"
            else:
                flash ("Invalid Username or Pasword!")
            
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
    session.pop('owner_id', None)
    return redirect(url_for('home'))


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
        

        # Assuming you handle file upload and save the file path
        picture = save_picture(request.files['picture'])

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

def save_picture(picture):
    # Ensure the 'static/uploads' folder exists in your project directory
    # Adjust the implementation based on your requirements
    picture_filename = secure_filename(picture.filename)
    picture_path = f'static/uploads/{picture_filename}'
    picture.save(picture_path)
    return picture_path








# @app.route('/delete_all_entries', methods=['GET', 'POST'])
# def delete_all_entries():
#     if request.method == 'GET':
#         try:
#             # Delete all entries in the User table
#             db.session.query(Car).delete()

#             # # Delete all entries in the Owner table
#             # db.session.query(user).delete()

#             # # Commit the changes to the database
#             db.session.commit()

#             # flash('All entries deleted successfully!')
#         except Exception as e:
#             # Handle exceptions if any
#             flash(f'Error deleting entries: {str(e)}')

#         return redirect(url_for('home'))  # Redirect to the home page or any other page

#     return render_template('delete_entries.html')  # Create a template for the delete_entries page
        
# @app.route('/delete_tables', methods=['GET', 'POST'])
# def delete_tables():
#     if request.method == 'GET':
#         try:
#             # Delete the User table
#             User.__table__.drop(db.engine)

#             # Delete the Owner table
#             Owner.__table__.drop(db.engine)

#             flash('Tables deleted successfully!')
#         except Exception as e:
#             # Handle exceptions if any
#             flash(f'Error deleting tables: {str(e)}')

#         return redirect(url_for('home'))  # Redirect to the home page or any other page

#     return render_template('delete_entries.html')  # Create 
if __name__ == "__main__":
    app.run(debug=True)