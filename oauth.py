from authlib.integrations.flask_client import OAuth
from flask import current_app

oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)

    # Register Google OAuth client
    oauth.register(
        name='google',
        client_id=current_app.config['GOOGLE_CLIENT_ID'],
        client_secret=current_app.config['GOOGLE_CLIENT_SECRET'],
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        refresh_token_url=None,
        redirect_uri=None,
        client_kwargs={
            'scope': 'openid profile email',
        }
    )

    # Register Facebook OAuth client
    oauth.register(
        name='facebook',
        client_id=current_app.config['FACEBOOK_CLIENT_ID'],
        client_secret=current_app.config['FACEBOOK_CLIENT_SECRET'],
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        refresh_token_url=None,
        redirect_uri=None,
        client_kwargs={
            'scope': 'email',
        }
    )

    # Register Twitter OAuth client
    oauth.register(
        name='twitter',
        client_id=current_app.config['TWITTER_CLIENT_ID'],
        client_secret=current_app.config['TWITTER_CLIENT_SECRET'],
        authorize_url='https://api.twitter.com/oauth/authenticate',
        authorize_params=None,
        access_token_url='https://api.twitter.com/oauth/access_token',
        access_token_params=None,
        refresh_token_url=None,
        redirect_uri=None,
        client_kwargs={
            'scope': 'email',
        }
    )

    # Register LinkedIn OAuth client
    oauth.register(
        name='linkedin',
        client_id=current_app.config['LINKEDIN_CLIENT_ID'],
        client_secret=current_app.config['LINKEDIN_CLIENT_SECRET'],
        authorize_url='https://www.linkedin.com/oauth/v2/authorization',
        authorize_params=None,
        access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
        access_token_params=None,
        refresh_token_url=None,
        redirect_uri=None,
        client_kwargs={
            'scope': 'r_liteprofile r_emailaddress',
        }
    )
