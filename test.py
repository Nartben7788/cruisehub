import unittest
from flask import Flask
from app import app, db, User, Owner, Car




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
        with app.app_context():
            try:
                # Explicitly roll back any database transactions
                db.session.rollback()
            except Exception as e:
                print(f"Error during rollback: {e}")

        # Remove the application context
        self.app_context.pop()

   

    def test_home_route(self):
        """Test the home route"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup_route(self):
        """Test the signup route"""
        response = self.app.post('/signup', data={
            'name': 'Test User2',
            'phone_number': '1234567890',
            'email': 'test@example.com',
            'username': 'testuser2',
            'password': 'testpassword',
            'user_type': 'user'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirection after signup

    def test_login_route(self):
        """Test the login route"""
        # Create a test user
        user = User(name='Test Userlog', phone_number='1234567890', email='test@examplelog.com',
                    username='testuserlog', password='testpassword', user_type='user')
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
            self.assertEqual(response.status_code, 302)
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

    def test_user_dashboard_authenticated(self):
        """Test user dashboard route for authenticated user"""
        with self.app as client:
            # Create a test user and add to the session
            with client.session_transaction() as session:
                user_id = 1  # Assuming user ID 1 for testing purposes
                session['user_id'] = user_id
                session['user_type'] = 'user'

            # Make a GET request to user_dashboard route
            response = client.get('/user_dashboard')

            # Check if the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

            # You can add more assertions to check specific content or behavior of the page

    def test_user_dashboard_unauthenticated(self):
        """Test user dashboard route for unauthenticated user"""
        with self.app as client:
            # Make a GET request to user_dashboard route without logging in
            response = client.get('/user_dashboard', follow_redirects=True)

            self.assertEqual(response.status_code, 200)

    def test_owner_dashboard_authenticated(self):
        """Test owner dashboard route for authenticated owner"""
        with self.app as client:
            # Create a test owner and add to the session
            with client.session_transaction() as session:
                owner_id = 1  # Assuming owner ID 1 for testing purposes
                session['user_id'] = owner_id
                session['user_type'] = 'owner'

            # Make a GET request to owner_dashboard route
            response = client.get(f'/owner/{owner_id}')

            # Check if the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

            # You can add more assertions to check specific content or behavior of the page

    def test_owner_dashboard_unauthenticated(self):
        """Test owner dashboard route for unauthenticated user"""
        with self.app as client:
            # Make a GET request to owner_dashboard route without logging in
            response = client.get('/owner/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_update_status_authenticated(self):
        """Test update_status route for authenticated owner"""
        with self.app as client:
            # Create a test owner and add to the session
            with client.session_transaction() as session:
                owner_id = 1  # Assuming owner ID 1 for testing purposes
                session['user_id'] = owner_id

            # Assuming there's a car with ID 1 for testing purposes
            car_id = 1

            # Make a POST request to update_status route
            response = client.post(f'/owner/{owner_id}/update_status/{car_id}')

            # Check if the response redirects to the owner_dashboard
            self.assertEqual(response.status_code, 302)
            self.assertIn(b'owner_dashboard', response.location)

          

    



if __name__ == '__main__':
    unittest.main()
