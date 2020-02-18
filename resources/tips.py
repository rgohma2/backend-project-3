import models 
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

tips = Blueprint('tips', 'tips')

@tips.route('/', methods=['GET'])
def tip_index():
	all_tips = models.Tip.select()

	tip_dicts = [model_to_dict(tip) for tip in all_tips]
	return jsonify(
			data=tip_dicts,
			message=f'retrieved {len(tip_dicts)} tips.',
			status=200
		), 200

@tips.route('/', methods=['POST'])
@login_required
def create_tip():
	payload = request.get_json()

	payload['creator'] = current_user.id
	tip = models.Tip.create(**payload)

	tip_dict = model_to_dict(tip)
	tip_dict['creator'].pop('password')

	# return 'hi'
	return jsonify(
			data=tip_dict,
			message='sucessfully created new tip',
			status=201
		), 201

@tips.route('/<id>', methods=['Delete'])
@login_required
def delete_tip(id):
	tip = models.Tip.get_by_id(id)
	if current_user.id == tip.creator.id:
		tip.delete_instance()
		return jsonify(
				data={},
				message='sucessfully deleted tip with id: {}'.format(tip.creator.id),
				status=200,
			), 200
	else:
		return jsonify(
				data={},
				message='error with user reference',
				status=403
			), 403

@tips.route('/<id>', methods=['PUT'])
@login_required
def update_tip(id):
	payload = request.get_json()

	tip = models.Tip.get_by_id(id)

	if tip.creator.id == current_user.id:
		tip.category = payload['category'] if 'category' in payload else None
		tip.tip = payload['tip'] if 'tip' in payload else None
		tip.description = payload['description'] if 'description' in payload else None

		tip.save()

		tip_dict = model_to_dict(tip)

		return jsonify(
				data=tip_dict,
				message='sucessfully updated tip at id: {}'.format(tip.creator.id),
				status=403
			), 403
	else:
		return jsonify(
				data={},
				message='error with user reference',
				status=403
			), 403







