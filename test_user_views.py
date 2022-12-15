"""User View tests."""

# run these tests like:
#
#    FLASK_DEBUG=False python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, Message, User, connect_db

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app, CURR_USER_KEY

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# This is a bit of hack, but don't use Flask DebugToolbar

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)

db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserBaseViewTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)
        db.session.flush()
        db.session.add_all([u1,u2])

        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

class UserHomePageTestCase(UserBaseViewTestCase):
    '''Tests view functions for the home page'''
    def test_home_page(self):
        '''Returns correct html for home page when logged in'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get('/', follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Logout", html)


    def test_home_page_logged_out(self):
        """Returns correct html for home page when logged out"""
        with self.client as c:
            resp = c.get('/', follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sign up now to get your own personalized timeline!", html)

class UserAuthorizationTestUseCase(UserBaseViewTestCase):
    '''Tests view functions for logging in and registering'''
    def test_login(self):
        '''Tests that correct HTML is returned when logging in'''
        with self.client as c:
            data = {"username": "u2", "password": "password"}
            resp = c.post('/login', data=data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hello, u2!", html)

    def test_login_bad_pass(self):
        '''Tests that correct HTML is returning when logging in with bad password'''
        with self.client as c:
            data = {"username": "u2", "password": "foo"}
            resp = c.post('/login', data=data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome back.", html)

    def test_login_bad_user(self):
        '''Tests that correct HTML is returning when logging in with bad user'''
        with self.client as c:
            data = {"username": "foo", "password": "password"}
            resp = c.post('/login', data=data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome back.", html)

    def test_logout(self):
        '''Tests that correct HTML is returning when logging out'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            resp = c.post('/logout', follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome back.", html)

    def test_logout_not_logged_in(self):
        '''Tests that correct HTML is returning when logging out but not logged in'''
        with self.client as c:
            resp = c.post('/logout', follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", html)

    def test_registration(self):
        '''Tests that correct HTML is returning when signing up'''
        with self.client as c:
            data = {"username": "u3", "password": "password",
                "email": "u3@email.com", "image_url": None}
            resp = c.post('/signup', data=data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@u3", html)

    def test_registration_duplicate_user(self):
        '''Tests that correct HTML is returning when signing up with duplicate user'''
        with self.client as c:
            data = {"username": "u2", "password": "password",
                "email": "foo@email.com", "image_url": None}
            resp = c.post('/signup', data=data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Username or email already taken", html)

    def test_registration_duplicate_email(self):
        '''Tests that correct HTML is returning when signing up with duplicate user'''
        with self.client as c:
            data = {"username": "foo", "password": "password",
                "email": "u2@email.com", "image_url": None}
            resp = c.post('/signup', data=data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Username or email already taken", html)

class UserProfileViewTestCase(UserBaseViewTestCase):
    '''Tests view functions for specific profiles'''
    def test_show_user(self):
        '''Tests that clicking a user profile returns the correct html'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            resp = c.get(f'/users/{self.u2_id}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('@u2', html)

    def test_show_user_not_logged_in(self):
        '''Tests that clicking a user profile returns the correct html when logged out'''
        with self.client as c:
            resp = c.get(f'/users/{self.u2_id}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized.', html)
    
    def test_list_users(self):
        '''Tests that route shows all users on the database'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            resp = c.get(f'/users', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('@u1', html)
            self.assertIn('@u2', html)
    
    def test_list_users_not_logged_in(self):
        '''Tests that list users returns correct html when logged out'''
        with self.client as c:
            resp = c.get(f'/users', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized.', html)

    def test_edit_profile(self):
        '''Tests that editing a profile returns the correct html'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            data = {"username": "new", "password": "password"}
            resp = c.post('/users/profile', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('@new', html)

    def test_edit_profile_invalid_email(self):
        '''Tests that editing a profile with an invalid email returns correct html'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            data = {"email": "new", "password": "password"}
            resp = c.post('/users/profile', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('Edit Your Profile', html)

    def test_edit_profile_not_logged_in(self):
        '''Tests that editing a profile while not logged in returns correct html'''
        with self.client as c:
            data = {"username": "new", "password": "password"}
            resp = c.post('/users/profile', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('Access unauthorized.', html)

    def test_delete_profile(self):
        '''Tests that deleting a profile returns the correct html and deletes the profile from the db'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            resp = c.post('/users/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Join Warbler today.', html)
            user = User.query.get(self.u1_id)
            self.assertIsNone(user)
    
    def test_delete_profile_not_logged_in(self):
        '''Tests that deleting a profile returns the correct html when not logged in'''
        with self.client as c:
            resp = c.post('/users/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized.', html)