import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user


users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test():
	return 'users resource working!'

@users.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	print(payload)

	payload['email'] = payload['email'].lower()

	try:

		models.User.get(models.User.email == payload['email'])

		return jsonify(
				data={},
				message='there is already a user registered with that email',
				status=401
			), 401

	except models.DoesNotExist:
		payload['password'] = generate_password_hash(payload['password'])
		new_user = models.User.create(**payload)
		login_user(new_user)

		user_dict = model_to_dict(new_user)
		user_dict.pop('password')

		return jsonify(
				data=user_dict,
				message='sucessfully registered new user with email: {}'.format(user_dict['email']),
				status=201
			), 201














