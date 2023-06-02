# Flask Warbler

This is the HTML rendering Flask application Warbler (Twitter clone). This project builds a RESTful API for handling users, messages, likes, follows, etc. in a similar manner to that seen on Twitter. It renders HTML that is stored and managed on the backend using Flask. This project currently has 96% test coverage.

## Table of Contents

- [Manual Installation](#manual-installation)
- [Commands](#commands)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)

## Manual Installation

To clone the repo:

    git clone https://github.com/youssefdoss/flask-warbler.git
    cd flask-warbler

To install the dependencies:

    pip3 install -r requirements.txt

Environment variables:

    SECRET_KEY=whatever_you_want
    DATABASE_URL=postgresql:///your_database_name

To seed database:

    python3 seed.py

## Commands

To run this in development:

    flask run -p (port of your choosing here)

To run the tests:

    python3 -m unittest

To generate the coverage report:

    coverage report -m

## Project Structure

generator\      # Creates/stores seed data
static\         # Static resources
templates\      # Jinja HTML templates
app.py          # Routes
forms.py        # Flask WTForms
models.py       # PSQL models

## API Endpoints

List of available routes:

**General routes**:\

`GET /` - Show homepage\

**Auth routes**:\
`POST signup` - Sign up user and send home\
`GET signup` - Get signup form\
`POST login` - Log in user and send home\
`GET login` - Get login form\
`POST logout` - Log out user\

**User routes**:\
`GET users` - Load page with list of users\
`GET users/<int:user_id>` - Load user profile\
`GET users/<int:user_id>/following` - Load list of users followed by specific user\
`GET users/<int:user_id>/followers` - Load list of followers of specific user\
`POST users/follow/<int:follow_id>` - Follow selected user\
`POST users/stop-following/<int:follow_id>` - Unfollow selected user\
`POST users/profile` - Update profile for current user\
`GET users/profile` - Get profile update form\
`POST users/delete` - Delete current user\

**Message routes**:\
`POST messages/new` - Add a message\
`GET messages/new` - Get new message form\
`GET messages/<int:message_id>` - Show a message\
`POST messages/<int:message_id>/delete` - Delete a message\

**Like routes**:\
`POST messages/<int:message_id>/like` - Handle like (without AJAX)
`POST messages/<int:message_id>/likes` - Handle like (with AJAX)
`GET users/<int:user_id>/likes` - Show user's likes