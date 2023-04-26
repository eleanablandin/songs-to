from flask import Flask, redirect, request, url_for, jsonify
from flask_oauthlib.client import OAuth
from flask import Blueprint


deezer_app = Blueprint('deezer_app', __name__)


#Deezer API keys 
deezer_keys = open('deezer.txt', 'r').read().splitlines()
id_key = deezer_keys[0]
secret_key = deezer_keys[1]


#Deezer crendential settings 
deezer = OAuth(deezer_app).remote_app(
    'deezer',
    consumer_key=id_key,
    consumer_secret=secret_key,
    base_url='https://api.deezer.com/',
    request_token_params={'scope': 'basic_access,email'},
    request_token_url=None,
    access_token_url='https://connect.deezer.com/oauth/access_token.php',
    authorize_url='https://connect.deezer.com/oauth/auth.php'
)


#Login fot the auth 
@deezer_app.route('/login')
def login():
    callback_url = request.url_root + 'callback'
    return deezer.authorize(callback=callback_url or None)

#Function to get token 
@deezer_app.route('/callback')
def callback():
    resp = deezer.authorized_response()

    if resp is None:
        return 'Access deny: Reason: {} error: {}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    access_token = resp['access_token']
    
    # file .txt
    with open('access_token.txt', 'w') as file:
        file.write(access_token)
    
    return redirect(url_for('deezer_app.home', access_token=access_token))


@deezer_app.route('/')
def home():
    with open('access_token.txt', 'r') as file:
        access_token = file.read()
    
    if access_token:
        return 'Token access: {}'.format(access_token)
    else:
        return 'Please, authorize your application in <a href="/login">login</a>'


