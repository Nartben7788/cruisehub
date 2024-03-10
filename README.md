# CruiseHub Application
Introduction

CruiseHub is a web application designed to facilitate car rental services. Users can sign up, log in, browse available cars, make reservations, and manage their reservations. Owners can list their cars, manage their listings, and view reservations made for their cars. The application is built using the Flask framework in Python.

# Features

User Authentication: Users can sign up, log in, and reset their passwords if forgotten.

Car Listings: Owners can list their cars with details such as make, model, price, and additional information.

Reservation System: Users can browse available cars and make reservations for specific dates.

Owner Dashboard: Owners can view and manage their car listings and reservations made for their cars.

Email Notifications: Users and owners receive email notifications for important events such as reservation confirmations and password resets.

# Code Structure
app.py: Contains the Flask application and all route definitions.

databases.py: Defines the database models using SQLAlchemy.

templates/: Contains HTML templates for rendering web pages.

static/: Contains static files such as CSS stylesheets and images.

# Database Management
Initialization: The database is initialized with sample data when the application starts.

Migration: Database migration scripts are provided to manage changes to the database schema.

# Notes
Security: User passwords are securely hashed using the generate_password_hash function from werkzeug.security to ensure data security.

Session Management: Flask session management is used to maintain user sessions and track logged-in users.

Error Handling: Error messages are displayed to users in case of validation errors or incorrect inputs.

File Uploads: Users can upload pictures of their cars during the listing process. Uploaded files are stored securely on the server.

# Contributors
Benjamin Teye Nartey
Toluwanimi Sonuga
Samson Oderinwale
Oluwadamilola Odeboje

# License
This project is not licensed.

# Contact
For any inquiries or support, please contact the development team at cruisehub.carhub@gmail.com.

# Acknowledgements
Special thanks to Mohammed Saudi(instructor) for his support during the development period.

# Website link: https://cruisehub-phi.vercel.app/