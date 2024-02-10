import unittest
from app import app, db, Car, User, Reservations
from datetime import datetime, timedelta

class TestReservationFunction(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db
        self.db.create_all()
        with app.app_context():
            self.db.create_all()
            
    def tearDown(self):
        with app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_get_method_user_logged_in(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.get('/reservation/1')
            self.assertEqual(response.status_code, 200)
            

    def test_get_method_user_not_logged_in(self):
        with self.app.test_client() as client:
            response = client.get('/reservation/1')
            self.assertEqual(response.status_code, 302)  # Redirect to login page
           
    def test_get_method_with_existing_reservations(self):
        # Add test logic for existing reservations
        pass

    def test_get_method_with_no_existing_reservations(self):
        # Add test logic for no existing reservations
        pass

    def test_post_method_user_not_logged_in(self):
        with self.app.test_client() as client:
            response = client.post('/reservation/1', data={'start_date': '2022-12-01', 'end_date': '2022-12-10'})
            self.assertEqual(response.status_code, 302)  # Redirect to login page
          

    def test_post_method_with_valid_input(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.post('/reservation/1', data={'start_date': '2022-12-01', 'end_date': '2022-12-10'})
            self.assertEqual(response.status_code, 302)  # Redirect to user_dashboard
            

    def test_post_method_with_invalid_input(self):
        
        pass

if __name__ == '__main__':
    unittest.main()