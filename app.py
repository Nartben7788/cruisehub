from flask import Flask, render_template, request, redirect, url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
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
        password = request.form['password']
        user_type = request.form['user_type']  

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if user_type == 'user':
            new_user = User(name=name, phone_number=phone_number, email=email, password=hashed_password)
            db.session.add(new_user)
        elif user_type == 'owner':
            new_owner = Owner(name=name, phone_number=phone_number, email=email, password=hashed_password)
            db.session.add(new_owner)

        db.session.commit()

        return redirect(url_for('home'))

    return render_template('signup.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        account_type = request.form['account_type']

        if account_type == "user":
            user = User.query.filter_by(user_name=user_name, password=password).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return "Login Successfull!"
            else:
                return "Invalid Username or Pasword!"
            
        elif account_type == "owner":
            owner = Owner.query.filter_by(user_name=user_name, password=password).first()
            if owner and bcrypt.checkpw(password.encode('utf-8'), owner.password.encode('utf-8')):
                return "Login Successful"
            else:
                return "Invalid Username or Pasword!"
        else:
            flash ("You must choose your Account Type")
        

if __name__ == "__main__":
    app.run(debug=True)