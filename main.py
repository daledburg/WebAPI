from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.user_controller import user_bp
from controllers.cli_controller import db_commands
from controllers.budget_controller import budget_bp
from controllers.cash_flow_controller import cash_flow_bp
import os


def create_app():
    app = Flask(__name__)

    app.config ['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(db_commands)
    app.register_blueprint(budget_bp)
    app.register_blueprint(cash_flow_bp)

    return app



