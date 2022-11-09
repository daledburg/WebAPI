from flask import Blueprint, jsonify, request, abort
from datetime import date, timedelta
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from models.saving import Saving, SavingSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

saving_bp = Blueprint('saving', __name__, url_prefix='/saving')

# Retrieve Users Savings accounts information
@saving_bp.route('/')
@jwt_required()
def get_savings():
    user_id = get_jwt_identity()
    stmt = db.select(Saving).filter_by(user_id = int(user_id))
    savings = db.session.scalars(stmt)

    return SavingSchema(many=True, only=['bank_name', 'current_amount']).dump(savings)

# Create new Savings account for user
@saving_bp.route('/', methods=['POST'])
@jwt_required()
def create_savings():
    data = SavingSchema().load(request.json)

    saving = Saving(
        bank_name = data['bank_name'],
        current_amount = data['current_amount'],
        date_updated = date.today(),
        user_id = get_jwt_identity()
    )

    db.session.add(saving)
    db.session.commit()

    return SavingSchema().dump(saving), 201

# Update savings account
@saving_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_savings(id):
    stmt = db.select(Saving).filter_by(id=id)
    saving = db.session.scalar(stmt)
    user_id = get_jwt_identity()
    if int(user_id) == int(saving.user_id):
        if saving:
            saving.bank_name = request.json.get('bank_name') or saving.bank_name
            saving.current_amount = request.json.get('current_amount') or saving.current_amount
            saving.date_updated = date.today()
            return SavingSchema(only=['bank_name', 'current_amount', 'date_updated']).dump(saving)
        else:
            return {'error': f'Card not found with id {id}'}, 404
    else:
        return {'error': 'Savings account not found'}, 404

# Delete Savings account connected to user
@saving_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_savings(id):
    stmt = db.select(Saving).filter_by(id=id)
    saving = db.session.scalar(stmt)
    user_id = get_jwt_identity()
    if int(user_id) == int(saving.user_id):
        if saving:
            db.session.delete(saving)
            db.session.commit()
            return {'message': 'Account successfully deleted'}
    else:
        return {'error': 'Account not found'}, 404


@saving_bp.route('/s/')
def get():
    stmt = db.select(Saving)
    savings = db.session.scalars(stmt)

    return SavingSchema(many=True, only=['bank_name', 'current_amount']).dump(savings)