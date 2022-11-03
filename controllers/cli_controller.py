from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.user import User
from models.cash_flow_items import CashFlowItem
from models.category import Category

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created successfully')

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables dropped')

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            f_name = 'Dale',
            l_name = 'Dahlenburg',
            email = 'dale.19@icloud.com',
            password = bcrypt.generate_password_hash('12345').decode('utf8'),
            date_created = date.today()
        ),
        User(
            f_name = 'Melanie',
            l_name = 'Campbell',
            email = 'mel_sheree@hotmail.com',
            password = bcrypt.generate_password_hash('ruby').decode('utf8'),
            date_created = date.today()
        ),
        User(
            f_name = 'Frank',
            l_name = 'Thomas',
            email = 'frankie@icloud.com',
            password = bcrypt.generate_password_hash('carol').decode('utf8'),
            date_created = date.today()
        ),
        User(
            f_name = 'Harry',
            l_name = 'Highpants',
            email = 'Harry@gmail.com',
            password = bcrypt.generate_password_hash('HighHigh').decode('utf8'),
            date_created = date.today()
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    cash_flow_items = [
        CashFlowItem(
            description = 'Wage',
            amount = int('1500'),
            date_created = date.today(),
            frequency = 'Weekly',
            user = users[0]
        ),
        CashFlowItem(
            description = 'Rent',
            amount = int('400'),
            date_created = date.today(),
            frequency = 'Fortnightly',
            user = users[0]
        ),
        CashFlowItem(
            description = 'Electricity',
            amount = int('200'),
            date_created = date.today(),
            frequency = 'Monthly',
            user = users[0]
        ),
        CashFlowItem(
            description = 'Car Loan',
            amount = int('155'),
            date_created = date.today(),
            frequency = 'Monthly',
            user = users[0]
        )
    ]

    db.session.add_all(cash_flow_items)
    db.session.commit()

    categories = [
        Category(
            is_income = True,
            cash_flow_item = cash_flow_items[0]
        ),
        Category(
            is_expense = True,
            cash_flow_item = cash_flow_items[1]
        ),
        Category(
            is_income = True,
            cash_flow_item = cash_flow_items[2]
        ),
        Category(
            is_outstanding_debt = True,
            is_expense = True,
            cash_flow_item = cash_flow_items[3]
        )
    ]

    db.session.add_all(categories)
    db.session.commit()
    print('Tables seeded')
