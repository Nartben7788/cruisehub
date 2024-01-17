from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

import bcrypt
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
            return redirect(url_for('home'))
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError: {e}")
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
                flash( "Login Successfull!", 'login')
            else:
                flash ("Invalid Username or Pasword!", 'login')
            
        elif user_type == "owner":
            owner = Owner.query.filter_by(username=username).first()
            if owner and check_password_hash(owner.password, password):
                return "Login Successful"
            else:
                return "Invalid Username or Pasword!"
        else:
            flash ("You must choose your Account Type")
    return render_template('login.html')











# @app.route('/delete_all_entries', methods=['GET', 'POST'])
# def delete_all_entries():
#     if request.method == 'GET':
#         try:
#             # Delete all entries in the User table
#             db.session.query(User).delete()

#             # Delete all entries in the Owner table
#             db.session.query(Owner).delete()

#             # Commit the changes to the database
#             db.session.commit()

#             flash('All entries deleted successfully!', 'delete)
#         except Exception as e:
#             # Handle exceptions if any
#             flash(f'Error deleting entries: {str(e)}', 'delete')

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
#             flash(f'Error deleting tables: {str(e)}', 'delete')

#         return redirect(url_for('home'))  # Redirect to the home page or any other page

#     return render_template('delete_entries.html')  # Create 
if __name__ == "__main__":
    app.run(debug=True)