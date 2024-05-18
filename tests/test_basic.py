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
    
    def test_post_page(self):
        with app.test_request_context('/'):  
            response = self.app.get(url_for('gallery'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        with app.test_request_context('/'): 
            response = self.app.get(url_for('login'))
        self.assertEqual(response.status_code, 200)
        
    def test_signup_page(self):
        with app.test_request_context('/'):  
            response = self.app.get(url_for('signup'))
        self.assertEqual(response.status_code, 200)
        
    def test_upload_page(self):
        with app.test_request_context('/'):  
            response = self.app.get(url_for('upload'))
        self.assertEqual(response.status_code, 302)

    def test_register_login_user(self):
        # Create a test user
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

        # Log in as the test user
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)

        # Check if the login was successful
        self.assertEqual(response.status_code, 200)
    
    def test_authenticated_user_access_upload(self):
        # Create a test user
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

        # Log in as the test user
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)

        # Check if the login was successful
        self.assertEqual(response.status_code, 200)


        # Access the upload page
        response = self.app.get('/upload')
        
        # Check if the user is redirected to the upload page
        self.assertEqual(response.status_code, 200) 
        
    
        
    
        
    



if __name__ == '__main__':
    unittest.main()
