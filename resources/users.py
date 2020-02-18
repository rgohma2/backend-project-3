import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict


users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test():
	return 'users resource working!'

@users.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	print(payload)

	return 'working'
