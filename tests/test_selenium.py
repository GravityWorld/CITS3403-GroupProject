import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from app import app, db
from config import TestConfig
from app.models import User

class FlaskAppSeleniumTestCase(unittest.TestCase):
    def setUp(self):
        # Configure the app for testing
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # Initialize the Selenium WebDriver
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword!')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        self.driver.get('http://127.0.0.1:5000/')
        self.assertIn('Welcome to Spyderweb!', self.driver.page_source)

    def test_login(self):
        self.driver.get('http://127.0.0.1:5000/login')
        username_field = self.driver.find_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password!')
        submit_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')

        username_field.send_keys('testuser')
        password_field.send_keys('testpassword!')
        submit_button.click()

        self.assertIn('testuser!', self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
