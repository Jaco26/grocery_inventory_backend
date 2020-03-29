from flask import Blueprint, abort
from flask_jwt_extended import jwt_required

from werkzeug.exceptions import HTTPException
from app.util import ApiResponse
from app.database.models import UnitOfMeasurement

unit_of_measure_bp = Blueprint('unit_of_measure', __name__)

@unit_of_measure_bp.route('/')
def get_units_of_measure():
  res = ApiResponse()
  try:
    res.data = UnitOfMeasurement.query.all()
  except HTTPException as exc:
    return exc
  except BaseException as exc:
    print(exc)
    abort(500)
  return res