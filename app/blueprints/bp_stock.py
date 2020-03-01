from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import HTTPException

from app.util import ApiResponse
from app.util.json_validation import (
  create_schema,
  should_look_like,
  Date
)
from app.database.models import Stock, FoodItem

stock_schema = create_schema({
  'name': str,
})

DATE_FMT = '%Y-%M-%D'
DATE_FMT_MSG = 'Date must be formatted: YYYY-MM-DD'

food_item_schema = create_schema({
  'food_kind_id': str,
  'date_item_was_new': Date(format=DATE_FMT, msg=DATE_FMT_MSG),
  'expiration_date': Date(format=DATE_FMT, msg=DATE_FMT_MSG),
})

stock_bp = Blueprint('stock_bp', __name__)

@stock_bp.route('/', methods=['POST'])
@stock_bp.route('/<stock_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def stock(stock_id=''):
  res = ApiResponse()
  try:
    if request.method == 'GET':
      stock = Stock.query.get_or_404(stock_id)
      res.data = {
        **stock.cols_dict(),
        'snapshots': [s for s in stock.snapshots.all()]
      }
    elif request.method == 'POST':
      body = should_look_like(stock_schema)
      stock = Stock(user_id=get_jwt_identity(), **body)
      stock.save()
      res.status = 201
    elif request.method == 'PUT':
      stock = Stock.query.get_or_404(stock_id)
      stock.name = body['name']
      stock.save()
      res.status = 201
    elif request.method == 'DELETE':
      stock = Stock.query.get_or_404(stock_id)
      stock.delete()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)
  return res


@stock_bp.route('/item/<stock_id>', methods=['POST'])
@stock_bp.route('/item/<stock_id>/<item_id>', methods=['DELETE'])
@jwt_required
def stock_item(stock_id='', item_id=''):
  res = ApiResponse()
  try:
    if request.method == 'POST':
      body = should_look_like(food_item_schema)
      stock = Stock.query.get_or_404(stock_id)
      if stock.user_id == get_jwt_identity():
        food_item = FoodItem({ 'stock_id': stock_id, **body })
        food_item.save()
        res.status = 201
      else:
        res.status = 401
        res.pub_msg = 'You do not have permission to add items to this stock'
    elif request.method == 'DELETE':
      food_item = FoodItem.query.get_or_404(item_id)
      food_item.delete()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)
  return res