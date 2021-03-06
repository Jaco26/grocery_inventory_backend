from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import HTTPException
from app.util import ApiResponse, uniform_name
from app.util.json_validation import create_schema, should_look_like, is_uuid, Coerce
from app.database.models import (
  FoodCategory,
  FoodKind,
  PackagingKind,
  PackagingState,
)
from app.database import helpers

food_category_schema = create_schema({
  'name': str,
})

food_kind_schema = create_schema({
  'name': str,
  'unit_of_measurement_id': is_uuid,
  ('serving_size', 0.0): Coerce(float),
})

packaging_kind_schema = create_schema({
  'name': str
})

packaging_state_schema = create_schema({
  'name': str
})

categories_bp = Blueprint('categories_bp', __name__)

@categories_bp.route('/food/category', methods=['GET', 'POST'])
@categories_bp.route('/food/category/<category_id>', methods=['PUT', 'DELETE'])
@jwt_required
def food_category(category_id=''):
  res = ApiResponse()
  try:
    if request.method == 'GET':
      res.data = [cat for cat in FoodCategory.query.all()]
    elif request.method == 'POST':
      body = should_look_like(food_category_schema)
      cat = FoodCategory(**body)
      cat.save()
      res.status = 201
    elif request.method == 'PUT':
      body = should_look_like(food_category_schema)
      cat = FoodCategory.query.get_or_404(category_id)
      cat.update_name(body['name'])
      cat.save()
    elif request.method == 'DELETE':
      cat =  FoodCategory.query.get_or_404(category_id)
      cat.delete()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)
  return res


@categories_bp.route('/food/kind', methods=['GET', 'POST'])
@categories_bp.route('/food/kind/<kind_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def food_kind(kind_id=''):
  res = ApiResponse()
  try:
    if request.method == 'GET':
      if kind_id:
        res.data = FoodKind.query.get_or_404(kind_id).full_dict()
      else:
        res.data = [x.full_dict() for x in FoodKind.query.filter_by(user_id=get_jwt_identity()).all()]
    elif request.method == 'POST':
      body = should_look_like(food_kind_schema)
      food_kind = FoodKind(**body)
      food_kind.user_id = get_jwt_identity()
      food_kind.save()
      res.status = 201
    elif request.method == 'PUT':
      body = should_look_like(food_kind_schema)
      food_kind = FoodKind.query.get_or_404(kind_id)
      if str(food_kind.user_id) != get_jwt_identity():
        res.status = 401
        res.pub_msg = 'You do not have permission to update this "food kind"'
      else:
        food_kind.update_name(body['name'])
        food_kind.unit_of_measurement_id = body['unit_of_measurement_id']
        food_kind.serving_size = body['serving_size']
        print(food_kind.unit_of_measurement_id)
        food_kind.save()
    elif request.method == 'DELETE':
      msg, status = helpers.delete_food_kind(kind_id=kind_id,
                              user_id=get_jwt_identity(),
                              force=request.args.get('force', False))
      res.pub_msg = msg
      res.status = status
  except HTTPException as exc:
    print(str(exc))
    return exc
  except BaseException as exc:
    print(exc)
    abort(500)
  return res


@categories_bp.route('/packaging/kind', methods=['GET', 'POST'])
@categories_bp.route('/packaging/kind/<kind_id>', methods=['PUT', 'DELETE'])
def packaging_kind(kind_id=''):
  res = ApiResponse()
  try:
    if request.method == 'GET':
      res.data = [x for x in PackagingKind.query.all()]
    elif request.method == 'POST':
      body = should_look_like(packaging_kind_schema)
      packaging_kind = PackagingKind(**body)
      packaging_kind.save()
      res.status = 201
    elif request.method == 'PUT':
      body = should_look_like(packaging_kind_schema)
      packaging_kind = PackagingKind.query.get_or_404(kind_id)
      packaging_kind.update_name(body['name'])
      packaging_kind.save()
    elif request.method == 'DELETE':
      packaging_kind = PackagingKind.query.get_or_404(kind_id)
      packaging_kind.delete()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)
  return res


@categories_bp.route('/food/kind')


@categories_bp.route('/packaging/state', methods=['GET', 'POST'])
@categories_bp.route('/packaging/state/<packaging_state_id>', methods=['PUT', 'DELETE'])
def packaging_state(packaging_state_id=''):
  res = ApiResponse()
  try:
    if request.method == 'GET':
      res.data = [x for x in PackagingState.query.all()]
    elif request.method == 'POST':
      body = should_look_like(packaging_kind_schema)
      packaging_state = PackagingState(**body)
      packaging_state.save()
      res.status = 201
    elif request.method == 'PUT':
      body = should_look_like(packaging_state_schema)
      packaging_state = PackagingState.query.get_or_404(packaging_state_id)
      packaging_state.update_name(body['name'])
      packaging_state.save()
    elif request.method == 'DELETE':
      packaging_state = PackagingState.query.get_or_404(packaging_state_id)
      packaging_state.delete()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)
  return res