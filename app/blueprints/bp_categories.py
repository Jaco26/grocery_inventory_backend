from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import HTTPException
from app.util import ApiResponse
from app.util.json_validation import create_schema, should_look_like
from app.database.models import (
  FoodCategory,
  FoodKind,
  PackagingKind,
)

food_category_schema = create_schema({
  'name': str,
})

food_kind_schema = create_schema({
  'name': str,
  'nutrition_info': dict,
  'notes': str,
})

packaging_kind_schema = create_schema({
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
      cat.name = body['name']
    elif request.method == 'DELETE':
      cat =  FoodCategory.query.get_or_404(category_id)
      cat.delete()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)


@categories_bp.route('/food/kind', methods=['GET', 'POST'])
@categories_bp.route('/food/kind/<kind_id>', methods=['PUT', 'DELETE'])
@jwt_required
def food_kind(kind_id=''):
  res = ApiResponse()
  try:
    if request.method == 'GET':
      res.data = [x.full_dict() for x in FoodKind.query.all()]
    elif request.method == 'POST':
      body = should_look_like(food_kind_schema)
      food_kind = FoodKind(**body)
      food_kind.save()
      res.status = 201
    elif request.method == 'PUT':
      body = should_look_like(food_kind_schema)
      food_kind = FoodKind.query.get_or_404(kind_id)
      food_kind.name = body['name']
      food_kind.nutrition_info = body['nutrition_info']
      food_kind.notes = body['notes']
      food_kind.save()
    elif request.method == 'DELETE':
      food_kind = FoodKind.query.get_or_404(category_id)
      food_kind.delete()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)


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
      packaging_kind.name = body['name']
    elif request.method == 'DELETE':
      packaging_kind = PackagingKind.query.get_or_404(kind_id)
      packaging_kind.delete()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)