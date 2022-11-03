from flask import Blueprint, jsonify, request
from datetime import date
from init import db
from models.cash_flow_items import CashFlowItem, CashFlowItemSchema
from flask_jwt_extended import get_jwt_identity, jwt_required

cash_flow_bp = Blueprint('cash_flow_items', __name__, url_prefix='/cashflow')

@cash_flow_bp.route('/')
def get_all_items():
    stmt = db.select(CashFlowItem).order_by(CashFlowItem.amount.desc())
    cash_flow_items = db.session.scalars(stmt)
    return CashFlowItemSchema(many=True).dump(cash_flow_items)

@cash_flow_bp.route('/', methods=['POST'])
# jwt_required()
def create_item():
    data = CashFlowItemSchema().load(request.json)
    cash_flow_item = CashFlowItem(
        description = data['description'],
        amount = data['amount'],
        date_created = date.today(),
        frequency = data['frequency'],
        # user_id = get_jwt_identity()
    )

    db.session.add(cash_flow_item)
    db.session.commit()

    return CashFlowItemSchema().dump(cash_flow_item), 201

@cash_flow_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
# jwt_required()
def update_item(id):
    stmt = db.select(CashFlowItem).filter_by(id=id)
    cash_flow_item = db.session.scalar(stmt)

    if cash_flow_item:
        cash_flow_item.description = request.json.get('description') or cash_flow_item.description
        cash_flow_item.amount = request.json.get('amount') or cash_flow_item.amount
        cash_flow_item.frequency = request.json.get('frequency') or cash_flow_item.frequency
        return CashFlowItemSchema().dump(cash_flow_item)
    else:
        return {'error': f'Card not found with id {id}'}, 404

@cash_flow_bp.route('/<int:id>/', methods=['DELETE'])
# jwt_required()
def delete_item(id):
    stmt = db.select(CashFlowItem).filter_by(id=id)
    cash_flow_item = db.session.scalar(stmt)

    if cash_flow_item:
        db.session.delete(cash_flow_item)
        db.session.commit()
        return {'message': f"Item '{cash_flow_item.description}' deleted successfully"}
    else:
        return {'error': f'Item not found with id {id}'}, 404





