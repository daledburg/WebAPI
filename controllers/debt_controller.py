from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.user import User
from models.cash_flow_items import CashFlowItem
from models.category import Category
from models.debt import Debt
from models.saving import Saving

debt_bp = Blueprint('debt', __name__, url_prefix='/debt')

