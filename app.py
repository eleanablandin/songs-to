from flask import Flask
from deezer import deezer_app

app = Flask(__name__)

flask_key = open('flask_key.txt', 'r').read().splitlines()
app.secret_key = flask_key[0]

app.register_blueprint(deezer_app)



if __name__ == '__main__':
    app.run()