from flask import Flask, jsonify

import models

from flask_login import LoginManager

from resources.users import users

DEBUG = True
PORT = 8000

app = Flask(__name__) 


app.register_blueprint(users, url_prefix='/api/v1/users')


app.secret_key = 'this is a key that is meant to be a secret. shhhhhh.'

login_manager = LoginManager()

login_manager.init_app(app)












if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)