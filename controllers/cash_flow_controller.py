from flask import Blueprint, request
from datetime import date
from init import db
from models.debt import Debt, DebtSchema
from models.cash_flow_items import CashFlowItem, CashFlowItemSchema
from flask_jwt_extended import get_jwt_identity, jwt_required

cash_flow_bp = Blueprint('cash_flow_items', __name__, url_prefix='/cashflow')

# Retrieve entered Incomes for User
@cash_flow_bp.route('/income/')
@jwt_required()
def get_incomes():
    user = get_jwt_identity()
    stmt = db.session.query(CashFlowItem).where(CashFlowItem.user_id == int(user))
    income = CashFlowItemSchema(many=True, exclude=['debt']).dump(stmt)
    user_incomes = [item for item in income if item.get('category_id') == 1]

    return user_incomes

# Retrieve entered Expenses for User
@cash_flow_bp.route('/expense/')
@jwt_required()
def get_expenses():
    user = get_jwt_identity()
    stmt = db.session.query(CashFlowItem).where(CashFlowItem.user_id == int(user))
    expense = CashFlowItemSchema(many=True).dump(stmt)
    user_expenses = [item for item in expense if item.get('category_id') != 1]

    return user_expenses

# Retrieve all items related to the logged in user
@cash_flow_bp.route('/')
@jwt_required()
def get_all_items():
    user_incomes = get_incomes()
    user_expenses = get_expenses()

    return [{'incomes': user_incomes}, {'expenses': user_expenses}]

# Retrieve only one item connected to user
@cash_flow_bp.route('/<int:id>/')
@jwt_required()
def get_one_cash_flow_item(id):
    user_id = get_jwt_identity()
    stmt = db.select(CashFlowItem).filter_by(id=id)
    one_item = db.session.scalar(stmt)
    if int(user_id) == int(one_item.user_id):
        return CashFlowItemSchema().dump(one_item)
    else:
        return {'error': 'Item does not exist for user'}

@cash_flow_bp.route('/debts/')
@jwt_required()
def get_debts():
    stmt = db.select(Debt)
    debts = db.session.scalars(stmt)

    debts_flow_id = DebtSchema(many=True, only=['cash_flow_item_id']).dump(debts)
    flow_list_ids = [i['cash_flow_item_id'] for i in debts_flow_id]
    print(flow_list_ids)

    user = get_jwt_identity()
    stmt = db.session.query(CashFlowItem).where(CashFlowItem.user_id == int(user))
    expense = CashFlowItemSchema(many=True).dump(stmt)
    user_debts = []
    for i in flow_list_ids:
        user_debts.append([item for item in expense if item.get('id') == i])

    return {"User Debts": user_debts}

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

#function to find weeklt amounts
def find_weekly_amount(items):
    item_list = []

    for i in items:
        print(i.get('amount'))
        if i.get('frequency') == 'Fortnightly':
            item_list.append(i.get('amount')/2)
        elif i.get('frequency') == 'Monthly':
            item_list.append(i.get('amount')/4)
        elif i.get('frequency') == 'Semi-annually':
            item_list.append(i.get('amount')/26)
        elif i.get('frequency') == 'Annually':
            item_list.append(i.get('amount')/52)
        elif i.get('frequency') == 'Weekly':
            item_list.append(i.get('amount'))

    return item_list

# Retrieve budget remainging
@cash_flow_bp.route('/budget/')
@jwt_required()
def get_current_budget():
    incomes = get_incomes()
    user_expenses = get_expenses()

    expense_list = find_weekly_amount(user_expenses)
    income_list = find_weekly_amount(incomes)

    budget_amount = sum(income_list) - sum(expense_list)

    return {"budget_remaining": f'Your remaining budget is ${budget_amount}'}
