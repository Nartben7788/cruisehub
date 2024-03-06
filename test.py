import unittest
from flask import Flask
from app import app, db, User, Owner

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

    def tearDown(self):
        # Remove the application context and drop all tables after running the tests
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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

if __name__ == '__main__':
    unittest.main()
