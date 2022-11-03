from flask import Blueprint, jsonify, request, abort
from datetime import date
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, jwt_required

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/register/', methods=['POST'])
def register_user():
    try:
        user = User(
            f_name = request.json.get('f_name'),
            l_name = request.json.get('l_name'),
            email = request.json.get('email'),
            password = bcrypt.generate_password_hash(request.json.get('password')),
            date_created = date.today()
        )
        # Add and commit user to db
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'User already exists with that email'}, 409

@user_bp.route('/')
def get_all_users():
    stmt = db.select(User).order_by(User.f_name)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)


