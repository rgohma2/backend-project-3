from flask import Flask, jsonify

import models

from flask_cors import CORS

from flask_login import LoginManager

from resources.users import users
from resources.tips import tips

DEBUG = True
PORT = 8000

app = Flask(__name__) 

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(tips, origins=['http://localhost:3000'], supports_credentials=True)



app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(tips, url_prefix='/api/v1/tips')


app.secret_key = 'this is a key that is meant to be a secret. shhhhhh.'

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	try:
		return models.User.get(models.User.id == user_id)
	except models.DoesNotExist:
		return None

@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(
			data={},
			message='no user is currently logged in',
			status=401
		), 401 





















if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)








