from sqlalchemy import desc
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import HTTPException
from app.util import ApiResponse
from app.util.json_validation import (
  create_schema,
  should_look_like,
  is_uuid,
)

from app.database.models import Stock, Snapshot, FoodItemState

snapshot_bp = Blueprint('snapshot_bp', __name__)

snapshot_schema = create_schema({
  'stock_id': is_uuid,
})

@snapshot_bp.route('/', methods=['POST'])
@jwt_required
def create_snapshot():
  res = ApiResponse()
  try:
    body = should_look_like(snapshot_schema)
    stock = Stock.query.get_or_404(body['stock_id'])
    if stock.user_id == get_jwt_identity():
      snapshot = Snapshot(**body)
      for food_item in stock.food_items:
        state = food_item.states.order_by(desc(FoodItemState.date_created)).first()
        snapshot.food_item_states.append(state)
      snapshot.save()
      res.status = 201
    else:
      res.status = 401
      res.pub_msg = 'You do not have permission to create a snapshot of this stock'
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    abort(500)
  return res