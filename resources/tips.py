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
				status=201
			), 201
	else:
		return jsonify(
				data={},
				message='error with user reference',
				status=403
			), 403

@tips.route('/<id>', methods=['POST'])
@login_required
def favorite_tip(id):

	tip = models.Tip.get_by_id(id)
	favs = [model_to_dict(fav) for fav in tip.favorites]
	# print(favs[0])

	already_favorited = False

	for fav in favs:
		if fav['user']['id'] == current_user.id:
			already_favorited = True

	if already_favorited != True:
		favorite = models.Favorite.create(
			user=current_user.id,
			tip=id)

		favorite_dict = model_to_dict(favorite)
		return jsonify(
				data=favorite_dict,
				message='favorited tip!',
				status=200
			), 200
	else:
		already_favorited = False
		return jsonify(
				data={},
				message='you can only favorite a tip once!',
				status=403
			), 403

@tips.route('/favorites', methods=['GET'])
def get_favorites():
	favorites = models.Favorite.select()
	favorite_dicts = [model_to_dict(fav) for fav in favorites]
	

	return jsonify(
			data=favorite_dicts,
			message='sucessfully retrieved {} favorites'.format(len(favorite_dicts)),
			status=201
		), 201







