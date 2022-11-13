from flask import Blueprint, request
from init import db
from models.cash_flow_items import CashFlowItem, CashFlowItemSchema
from models.debt import Debt, DebtSchema
from flask_jwt_extended import get_jwt_identity, jwt_required

debt_bp = Blueprint('debt', __name__, url_prefix='/debt')

# Retrieve all expenses that are outstanding debts for user
@debt_bp.route('/')
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

# Add debt information to an already existing expense
@debt_bp.route('/<int:id>/', methods=['POST'])
@jwt_required()
def create_debt(id):
    data = DebtSchema().load(request.json)
    stmt = db.select(CashFlowItem).filter_by(id=id)
    cash_flow_item = db.session.scalar(stmt)

    user = get_jwt_identity()

    # Check if belongs to logged in user
    if int(user) == int(cash_flow_item.user_id):
        # Create new instance of debt
        debt_item = Debt(
            outstanding_amount = data['outstanding_amount'],
            cash_flow_item_id = id
        )
        # Add and commit to database
        db.session.add(debt_item)
        db.session.commit()
        return DebtSchema().dump(debt_item), 201
    else:
        return {'error': 'Not your Item'}, 404

# Update Debt information
@debt_bp.route('/<int:id>/', methods=['PATCH', 'PUT'])
@jwt_required()
def update_debt(id):

    stmt = db.select(CashFlowItem).filter_by(id=id)
    cash_flow_item = db.session.scalar(stmt)

    stmt1 = db.select(Debt).filter_by(cash_flow_item_id=id)
    debt_item = db.session.scalar(stmt1)

    user = get_jwt_identity()

    # Check if belongs to logged in user
    if int(user) == int(cash_flow_item.user_id):
        if debt_item:
            # Update required values in database
            debt_item.outstanding_amount = request.json.get('outstanding_amount') or debt_item.outstanding_amount
            db.session.commit()
            return DebtSchema().dump(debt_item), 201
    else:
        return {'error': 'Not your Item'}, 404

# Delete debt information
@debt_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_debt(id):

    stmt = db.select(CashFlowItem).filter_by(id=id)
    cash_flow_item = db.session.scalar(stmt)

    stmt1 = db.select(Debt).filter_by(cash_flow_item_id=id)
    debt_item = db.session.scalar(stmt1)

    user = get_jwt_identity()

    # Check if belongs to logged in user
    if int(user) == int(cash_flow_item.user_id):
        if debt_item:
            # Delete from Database
            db.session.delete(debt_item)
            db.session.commit()
            return {'message': "Debt item deleted successfully"}
    else:
        return {'error': 'Not your Item'}, 404




