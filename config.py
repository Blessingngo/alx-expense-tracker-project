import os
import secrets

class Config:
    SECRET_KEY = os.urandom(24)
    GOOGLE_CLIENT_ID = 'your-google-client-id'
    GOOGLE_CLIENT_SECRET = 'your-google-client-secret'
    FACEBOOK_CLIENT_ID = 'your-facebook-client-id'
    FACEBOOK_CLIENT_SECRET = 'your-facebook-client-secret'
    TWITTER_CLIENT_ID = 'your-twitter-client-id'
    TWITTER_CLIENT_SECRET = 'your-twitter-client-secret'
    LINKEDIN_CLIENT_ID = 'your-linkedin-client-id'
    LINKEDIN_CLIENT_SECRET = 'your-linkedin-client-secret'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'blessing0107'
    MYSQL_DB = 'bblexpense'
    SECRET_KEY = secrets.token_hex(24)

