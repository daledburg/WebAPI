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
    data = UserSchema().load(request.json)
    try:
        user = User(
            f_name = data['f_name'],
            l_name = data['l_name'],
            email = data['email'],
            password = bcrypt.generate_password_hash(data['password']),
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

# Update or delete user details and associated information
@user_bp.route('/<int:id>/', methods=['PUT', 'PATCH', 'DELETE'])
@jwt_required()
def update_user(id):
    data = UserSchema().load(request.json)
    
    stmt = db.select(User).filter_by(id=id)
    user_details = db.session.scalar(stmt)
    
    user = get_jwt_identity()

    # Check if belongs to logged in user
    if int(user) == int(user_details.id):
        if request.method == ('PUT' or 'PATCH'):
            if user_details:
                # Update required values in database
                user_details.f_name = data['f_name'] or user_details.f_name
                user_details.l_name = data['l_name'] or user_details.l_name
                user_details.email = data['email'] or user_details.email
                user_details.password = bcrypt.generate_password_hash(data['password']) or user_details.password
                return UserSchema(only=['f_name', 'l_name', 'email']).dump(user_details)
            else:
                return {'error': f'User not found with id {id}'}, 404
        elif request.method == 'DELETE':
            if user_details:
                # Delete item from database
                db.session.delete(user_details)
                db.session.commit()
                return {'message': f'User {user_details.email} deleted successfully'}
            else:
                return {'error': f'User {user_details.email} not found.'}, 404
    else:
        return {'error': 'User not found'}, 404
