from flask import Blueprint, jsonify, request
from datetime import date
from init import db
import collections
from models.cash_flow_items import CashFlowItem, CashFlowItemSchema
from models.category import CategorySchema, Category
from flask_jwt_extended import get_jwt_identity, jwt_required

cash_flow_bp = Blueprint('cash_flow_items', __name__, url_prefix='/cashflow')

# Function to authorise if item belongs to currently loggen in user
def authorize(flow_type):
    users_list = []
    user = get_jwt_identity()
    schema_dump = CategorySchema(only=['cash_flow_items']).dump(flow_type)
    cash_items_dump = schema_dump.get('cash_flow_items')
    w = 0
    for i in cash_items_dump:
        for k, v in i.items():
            if (k == 'user_id'):
                if v == int(user):
                    users_dict = cash_items_dump[w]
                    users_dict_copy = users_dict.copy()
                    users_list.append(users_dict_copy)
                    w = w + 1

    return users_list

# Retrieve all items related to the logged in user
@cash_flow_bp.route('/')
@jwt_required()
def get_all_items():
    stmt = db.select(Category).filter_by(id=1)
    incomes = db.session.scalar(stmt)
    income_list = authorize(incomes)

    stmt1 = db.select(Category).filter_by(id=2)
    expenses = db.session.scalar(stmt1)
    expense_list = authorize(expenses)

    return [{'incomes': income_list}, {'expenses': expense_list}]

# Retrieve entered Incomes for User
@cash_flow_bp.route('/income/')
@jwt_required()
def get_incomes():
    stmt = db.select(Category).filter_by(id=1)
    incomes = db.session.scalar(stmt)
    income_list = authorize(incomes)

    return income_list

# Retrieve entered Expenses for User
@cash_flow_bp.route('/expense/')
@jwt_required()
def get_expenses():
    stmt = db.select(Category).filter_by(id=2)
    expenses = db.session.scalar(stmt)
    expense_list = authorize(expenses)

    return expense_list

# Create new entry in database for new item
@cash_flow_bp.route('/<int:id>', methods=['POST'])
@jwt_required()
def create_item(id):

    data = CashFlowItemSchema().load(request.json)

    cash_flow_item = CashFlowItem(
        description = data['description'],
        amount = data['amount'],
        date_created = date.today(),
        frequency = data['frequency'],
        user_id = get_jwt_identity(),
        category_id = id
    )

    db.session.add(cash_flow_item)
    db.session.commit()

    return CashFlowItemSchema().dump(cash_flow_item), 201

# Update current item in database if belogns to logged in user
@cash_flow_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_item(id):
    stmt = db.select(CashFlowItem).filter_by(id=id)
    cash_flow_item = db.session.scalar(stmt)
    user = get_jwt_identity()
    if int(user) == int(cash_flow_item.user_id):
        if cash_flow_item:
            cash_flow_item.description = request.json.get('description') or cash_flow_item.description
            cash_flow_item.amount = request.json.get('amount') or cash_flow_item.amount
            cash_flow_item.frequency = request.json.get('frequency') or cash_flow_item.frequency
            return CashFlowItemSchema(only=['description', 'amount', 'frequency']).dump(cash_flow_item)
        else:
            return {'error': f'Card not found with id {id}'}, 404
    else:
        return {'error': 'Card not yours!'}, 404

# Delete item if belongs to logged in user
@cash_flow_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_item(id):
    stmt = db.select(CashFlowItem).filter_by(id=id)
    cash_flow_item = db.session.scalar(stmt)
    user = get_jwt_identity()
    if int(user) == int(cash_flow_item.user_id):
        if cash_flow_item:
            db.session.delete(cash_flow_item)
            db.session.commit()
            return {'message': f"Item '{cash_flow_item.description}' deleted successfully"}
        else:
            return {'error': f'Item not found with id {id}'}, 404
    else:
        return {'error': 'Card not yours!'}, 404

@cash_flow_bp.route('/budget/')
@jwt_required()
def get_current_budget():
    stmt = db.select(Category).filter_by(id=1)
    incomes = db.session.scalar(stmt)
    income_list = authorize(incomes)

    stmt1 = db.select(Category).filter_by(id=2)
    expenses = db.session.scalar(stmt1)
    expense_list = authorize(expenses)

    counter_expense = collections.Counter()
    for d in expense_list:
        counter_expense.update(d)

    result = dict(counter_expense)
    total_expense = result.get('amount')

    income_counter = collections.Counter()
    for d in income_list:
        income_counter.update(d)

    result = dict(income_counter)
    total_income = result.get('amount')

    return {"budget_remaining": f'Your remaining budget is ${total_income - total_expense}'}