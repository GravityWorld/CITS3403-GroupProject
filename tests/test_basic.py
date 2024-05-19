import unittest
from app import app, db
from config import TestConfig
from flask import url_for
from app.models import User


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            
    ## SECTION TO CHECK IF EVERY PAGE CAN BE ACCESSED (WITH AND WITHOUT AUTHNETICATION)

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Spyderweb', response.data)
    
    def test_post_page(self):
        with app.test_request_context('/'):  
            response = self.app.get(url_for('gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gallery', response.data)
        
    def test_login_page(self):
        with app.test_request_context('/'): 
            response = self.app.get(url_for('login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log into your account', response.data)
        
    def test_signup_page(self):
        with app.test_request_context('/'):  
            response = self.app.get(url_for('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create an Account', response.data)
        
    def test_upload_page_without_authentication(self):
        with app.test_request_context('/'):  
            response = self.app.get(url_for('upload'))
        self.assertEqual(response.status_code, 302)
       

    def test_register_login_user(self):
        # Create a test user
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password!')
            db.session.add(user)
            db.session.commit()

        # Log in as the test user
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='password!'
        ), follow_redirects=True)

        # Check if the login was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SPYDERWEB', response.data)
    
    def test_authenticated_user_access_upload(self):
        # Create a test user
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password!')
            db.session.add(user)
            db.session.commit()

        # Log in as the test user
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='password!'
        ), follow_redirects=True)

        # Check if the login was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SPYDERWEB', response.data)

        # Access the upload page
        response = self.app.get('/upload')
        
        # Check if the user is redirected to the upload page
        self.assertEqual(response.status_code, 200) 
        self.assertIn(b'Upload your Code', response.data)

        
    def test_logout(self):
        # Register and log in a new user
        self.app.post('/signup', data=dict(
            username='testuser',
            email='test@example.com',
            password='password!',
            confirm='password!'
        ), follow_redirects=True)

        self.app.post('/login', data=dict(
            username='testuser',
            password='password!'
        ), follow_redirects=True)

        # Log out the user
        response = self.app.get('/logout', follow_redirects=True)

        # Check if the logout was successful
        self.assertEqual(response.status_code, 200)
        
    
    def test_invalid_login(self):
        # Try to log in with invalid credentials
        response = self.app.post('/login', data=dict(
            username='wronguser', # this is a user that is not registered
            password='wrongpassword'
        ), follow_redirects=True)

        # Check if the login attempt was unsuccessful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)  
        
    ## SECTION FOR DATABASE TESTS
    
    def test_user_creation(self):
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

            # Query the user from the database
            user_from_db = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user_from_db)
            self.assertEqual(user_from_db.email, 'test@example.com')
            
    def test_duplicate_user_creation(self):
        with app.app_context():
            # Create the first user
            user1 = User(username='testuser', email='test1@example.com')
            user1.set_password('password')
            db.session.add(user1)
            db.session.commit()

            # Attempt to create a second user with the same username
            user2 = User(username='testuser', email='test2@example.com')
            user2.set_password('password')
            db.session.add(user2)

            # Assert that an exception is raised when trying to commit the second user
            with self.assertRaises(Exception):
                db.session.commit()
            
            # Rollback the session to clean up
            db.session.rollback()

    def test_user_update(self):
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

            # Update the user's email
            user.email = 'newemail@example.com'
            db.session.commit()

            # Query the updated user from the database
            user_from_db = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user_from_db)
            self.assertEqual(user_from_db.email, 'newemail@example.com')      



if __name__ == '__main__':
    unittest.main()
