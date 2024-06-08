from flask import redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_login import login_user, logout_user, login_required
from models import User, users

def setup_routes(app):
    oauth = OAuth(app)

    @app.route('/')
    def index():
        return 'Welcome to the Expense Tracker!'

    @app.route('/login/<provider>')
    def login(provider):
        if provider not in oauth._clients:
            return 'Provider not supported', 400
        redirect_uri = url_for(f'{provider}_authorized', _external=True)
        return oauth.create_client(provider).authorize_redirect(redirect_uri)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/login/<provider>/authorized')
    def authorized(provider):
        client = oauth.create_client(provider)
        if not client:
            return 'Provider not supported', 400
        
        token = client.authorize_access_token()
        if token is None:
            return 'Access denied', 403
        
        user_info = client.parse_id_token(token)
        if provider == 'google':
            user_data = {
                'id': user_info['sub'],
                'name': user_info['name'],
                'email': user_info['email']
            }
        elif provider == 'facebook':
            user_data = client.get('me?fields=id,name,email').json()
        elif provider == 'twitter':
            user_data = client.get('account/verify_credentials.json').json()
        elif provider == 'linkedin':
            user_data = client.get('v2/me').json()
            email_data = client.get('v2/emailAddress?q=members&projection=(elements*(handle~))').json()
            user_data['email'] = email_data['elements'][0]['handle~']['emailAddress']
        else:
            return 'Provider not supported', 400

        user = User(id=user_data['id'], name=user_data['name'], email=user_data['email'])
        users[user.id] = user
        login_user(user)
        return redirect(url_for('index'))
