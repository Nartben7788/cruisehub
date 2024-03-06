import unittest
from flask import Flask
from app import app, db, User, Owner, Car

import unittest
from app import app, db


class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()

        # Establish an application context before running the tests
        self.app_context = app.app_context()
        self.app_context.push()

        # Create all tables in the database
        db.create_all()

    # def tearDown(self):
    #     # Remove the application context and drop all tables after running the tests
    #     db.session.remove()
    #     db.drop_all()
    #     self.app_context.pop()

    # Write your test cases here

    def test_home_route(self):
        """Test the home route"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup_route(self):
        """Test the signup route"""
        response = self.app.post('/signup', data={
            'name': 'Test User',
            'phone_number': '1234567890',
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'user_type': 'user'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirection after signup

    def test_login_route(self):
        """Test the login route"""
        # Create a test user
        user = User(name='Test User', phone_number='1234567890', email='test@example.com',
                    username='testuser', password='testpassword', user_type='user')
        db.session.add(user)
        db.session.commit()

        # Attempt login with correct credentials
        response = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword',
            'user_type': 'user'
        })
        self.assertEqual(response.status_code, 200)  # Check for redirection after login

        # Attempt login with incorrect credentials
        response = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword',
            'user_type': 'user'
        })
        self.assertEqual(response.status_code, 200)  # Should remain on the login page

    def test_logout_route(self):
        """Test the logout route"""
        with self.app as client:
            with client.session_transaction() as session:
                session['user_id'] = 1
                session['user_type'] = 'user'

            response = client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)  # Should return to the login page

    def test_add_car_authenticated(self):
        """Test adding a car when the owner is authenticated"""

        # Create a test owner
        test_owner_id = 1  # Assuming owner ID 1 for testing purposes

        # Log in the test owner
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user_id'] = test_owner_id

            # Make a POST request to add a car
            response = c.post('/add_car', data={
                'model': 'Test Model',
                'make': 'Test Make',
                'price': '10000',
                'additional_info': 'Test additional info',
                'picture': 'car1.jpg' # You may need to adjust this
            }, follow_redirects=True)

            # Check if the car is added successfully
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Model', response.data)  # Check for model name in response

            # Check if the car is added to the database
            car = Car.query.filter_by(model='Test Model').first()
            self.assertIsNotNone(car)
            self.assertEqual(car.make, 'Test Make')

    def test_add_car_not_authenticated(self):
        """Test adding a car when the owner is not authenticated"""

        # Make a GET request to add a car without logging in
        response = self.app.get('/add_car', follow_redirects=True)

        # Check if the user is redirected to the login page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()
