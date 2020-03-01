from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import HTTPException
from app.util import ApiResponse
from app.util.json_validation import create_schema, should_look_like

food_item_bp = Blueprint('food_item', __name__)