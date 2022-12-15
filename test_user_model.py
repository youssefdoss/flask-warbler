"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, connect_db

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        '''Ensures that initialized user has no messages or followers'''
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test_is_following_true(self):
        '''Tests that is_following detects followers properly'''
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)
        
        u1.following.append(u2)

        following = u1.is_following(u2)

        self.assertEqual(following, True)
    
    def test_is_following_false(self):
        '''Tests that is_following detects non-followers properly'''
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        following = u1.is_following(u2)

        self.assertEqual(following, False)
    
    def test_is_followed_by_true(self):
        '''Tests that is_followed_by detects followers properly'''
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u2.following.append(u1)

        followed_by = u1.is_followed_by(u2)

        self.assertEqual(followed_by, True)
    
    def test_is_followed_by_false(self):
        '''Tests that is_followed_by detects non-followers properly'''
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        followed_by = u1.is_followed_by(u2)

        self.assertEqual(followed_by, False)
    
    def test_signup_success(self):
        '''Tests that User.signup returns a User instance with valid inputs'''
        user = User.signup(username='test_username', email='test@test.com', password='test_password')

        self.assertIsInstance(user, User)
    
    def test_signup_failure(self):
        # TODO: Fix this
        '''Tests that User.signup does not returns a User instance with invalid inputs'''
        user = User.signup(username='test_username', email=None, password='test_password')

        self.assertNotIsInstance(user, User)