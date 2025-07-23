# First is the “various configurations” that we’ll have. Now what r these configurations? We need to connect our flask app with the database, with flask-security, so all such configurations will be done in the config file.
class Config:
    DEBUG = False # When True: You get detailed error messages in the browser. In production: Set to False to avoid exposing errors to users.
    SQLALCHEMY_TRACK_MODIFICATIONS = True # Enables tracking of object changes in SQLAlchemy. Note: It's not needed unless you’re using signals. Set to False to save memory and avoid warnings.
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '21f3002082@ds.study.iitm.ac.in'
    MAIL_PASSWORD = 'ywaz mofw kjpc yfhm'
    MAIL_DEFAULT_SENDER = '21f3002082@ds.study.iitm.ac.in'

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lmsv2.sqlite3' # Tells Flask the location of the database. Here: It's using a local SQLite database file named lmsv2.sqlite3.
    DEBUG = True
    # Config for security
    SECRET_KEY = "your_secret_key_here" # Used to secure sessions and cookies. Needed for features like flask-login, session encryption, and CSRF protection.
    SECURITY_PASSWORD_HASH = "pbkdf2_sha256" # Hashing algorithm to use for passwords
    SECURITY_PASSWORD_SALT = "your_salt_here" # Helps us to add an extra layer of security to the password hashing. Makes hashes more secure, even if two users have the same password.
    WTF_CSRF_ENABLED = False # Controls whether CSRF protection is enabled. When False: Disables CSRF tokens in forms (often done in development or APIs).
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token" # Defines the HTTP header used for token-based login/authentication. Helpful when building APIs that use tokens instead of sessions.

class ProductionDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lmsv2_prod.sqlite3'  # Change to your production DB URI
    DEBUG = False
    SECRET_KEY = "your_production_secret_key_here"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha256"
    SECURITY_PASSWORD_SALT = "your_production_salt_here"
    WTF_CSRF_ENABLED = True  # Enable CSRF protection in production
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
