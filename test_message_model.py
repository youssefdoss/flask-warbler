"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
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

class MessageModelTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        m1 = Message(text = "foo")
        m2 = Message(text = "bar")

        u1.messages.append(m1)
        u2.messages.append(m2)
        u1.liked_messages.append(m2)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.m1_id = m1.id
        self.m2_id = m2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_message_model(self):
        '''Ensures that message has associated user and text'''
        u1 = User.query.get(self.u1_id)
        m1 = Message.query.get(self.m1_id)

        self.assertEqual(len(u1.messages), 1)
        self.assertEqual(m1.text, "foo")

    def test_like_model(self):
        '''Ensures that liked messages appear in user's liked messages'''
        u1 = User.query.get(self.u1_id)
        m1 = Message.query.get(self.m1_id)
        m2 = Message.query.get(self.m2_id)

        self.assertIn(m2, u1.liked_messages)
        self.assertNotIn(m1, u1.liked_messages)