from flask import Flask  # Imports the Flask class to create the app instance
from flask_security import Security, SQLAlchemyUserDatastore, hash_password  # Imports Flask-Security classes for user auth and role-based access control
# from flask_security.datastore import SQLAlchemyUserDatastore 
# from flask_security.utils import hash_password  # Imports Flask-Security classes for user auth and role-based access control
# from werkzeug.security import generate_password_hash

# Imports from other code files
from application.database import db  # Imports the database instance (usually SQLAlchemy)
from application.models_4 import User, Role  # Imports User and Role models used for authentication
from application.config import LocalDevelopmentConfig  # Imports local development configuration settings
# from application.resources import api


def create_app():
    app = Flask(__name__)  # Creates the Flask app instance
    app.config.from_object(LocalDevelopmentConfig)  # Applies the local development configuration to the app. But we may need to change this to ProductionConfig when we deploy the app.
    db.init_app(app)  # Initializes the database extension with the app
    # api.init_app(app)
    # Creates a user datastore linking the database with the User and Role models
    datastore = SQLAlchemyUserDatastore(db, User, Role) # Also, the datastore is used to pre-fill the values like fs_uniquifier, active. We won't manually set these values. 

    # Initializes Flask-Security with the app and the datastore for user management and security features
    app.security = Security(app, datastore) 

    # Pushes an application context to make `current_app`, `g`, and other context-bound objects available
    app.app_context().push()

    return app  # Returns the configured Flask app instance

app = create_app()  # Calls the function to create and configure the app

with app.app_context():  # Ensures the app context is available for database operations
    # THE MOMENT OUR APP STARTS RUNNING, FOLLOWING ENTRIES WILL ALWAYS BE PRESENT IN THE DATABASE. WE DON'T NEED TO MANUALLY DO ANYTHING.
    db.create_all()  # Creates all database tables defined in the models if they do not exist
    
    app.security.datastore.find_or_create_role(name='admin', description='Superuser of app') # "find_or_create_role" checks if the role exists, and if not, creates it 
    app.security.datastore.find_or_create_role(name='user', description='General user of the app') 
    db.session.commit()  # Commits the changes to the database, ensuring roles are saved. WE CANNOT EXECUTE THE BELOW LINES BEFORE THE THIS FIRST COMMIT.

    if not app.security.datastore.find_user(email="user0@admin.com"): 
        app.security.datastore.create_user( 
            email="user0@admin.com",
            # username = "admin01",
            password = hash_password("1234"),
            role = "admin"
        ) 
    if not app.security.datastore.find_user(email="user1@user.com"):
        app.security.datastore.create_user( 
            email="user1@user.com",
            # username = "user01",
            password = hash_password("1234"),
            role = "user"
        ) 
    db.session.commit()

from application.routes import *

if __name__ == "__main__":  # Ensures this block runs only if the script is executed directly
    app.run()  # Starts the Flask development server