from flask import Blueprint, jsonify, request, abort
from datetime import date
from init import db, bcrypt
from models.budget import Budget, BudgetSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required

budget_bp = Blueprint('budget', __name__, url_prefix='/budget')

@budget_bp.route('/')
def get_budget():
    stmt = db.select(Budget).order_by(Budget.id)
    budgets = db.session.scalars(stmt)
    return BudgetSchema(many=True).dump(budgets)

