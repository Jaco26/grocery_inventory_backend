from pprint import pprint
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import HTTPException
from app.util import ApiResponse
from app.util.json_validation import create_schema, should_look_like, is_uuid
from app.database.models import StockItemState

food_item_state_bp = Blueprint('food_item_state', __name__)

food_item_state_schema = create_schema({
  'food_item_id': is_uuid,
  'packaging_kind_id': is_uuid,
  'packaging_state_id': is_uuid,
  'quantity': int
})

@food_item_state_bp.route('/', methods=['POST'])
@jwt_required
def food_item_state():
  res = ApiResponse()
  try:
    body = should_look_like(food_item_state_schema)
    food_item_state = StockItemState(**body)
    food_item_state.save()
    res.status = 201
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    print(exc)
    abort(500)
  return res