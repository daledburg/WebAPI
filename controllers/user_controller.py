from flask import Blueprint, jsonify, request, abort
from datetime import date, timedelta
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__, url_prefix='/user')

# Register and create new user
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

# Get logged in users information
@user_bp.route('/userinfo/')
@jwt_required()
def get_user_info():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id = int(user_id))
    user_info = db.session.scalar(stmt)
    return UserSchema(exclude=['password']).dump(user_info)

# Login 
@user_bp.route('/login/', methods=['POST'])
def user_login():
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=12))
        return {'email': user.email, 'token': token}
    else:
        return {'error': 'Invalid email or password'}, 401
