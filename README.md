# CruiseHUB
CruiseHUB seeks to simplify the car rental process, making it more accessible for users to secure reliable transportation facilities.

HOW TO RUN THE APP.

To run the app, install and do the following:

- Pip install Flask-SQLAlchemy
- Pip install Flask-Migrate
- Pip install flask_session

The following 3 steps will be needed as we update the database schema:

flask db init
flask db migrate -m "initial migration"
flask db upgrade
