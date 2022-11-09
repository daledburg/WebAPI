from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.user import User
from models.cash_flow_items import CashFlowItem
from models.category import Category
from models.debt import Debt
from models.saving import Saving


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
    categories = [
        Category(
            is_income = True,
            is_expense = False
        ),
        Category(
            is_income = False,
            is_expense = True
        )
    ]

    db.session.add_all(categories)
    db.session.commit()

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
            user = users[0],
            category_id = 1
        ),
        CashFlowItem(
            description = 'Crypto',
            amount = int('200'),
            date_created = date.today(),
            frequency = 'Weekly',
            user = users[1],
            category_id = 1
        ),
        CashFlowItem(
            description = 'Rent',
            amount = int('400'),
            date_created = date.today(),
            frequency = 'Fortnightly',
            user = users[0],
            category_id = 2
        ),
        CashFlowItem(
            description = 'Electricity',
            amount = int('200'),
            date_created = date.today(),
            frequency = 'Monthly',
            user = users[0],
            category_id = 2
        ),
        CashFlowItem(
            description = 'Car Loan',
            amount = int('155'),
            date_created = date.today(),
            frequency = 'Monthly',
            user = users[0],
            category_id = 2
        ),
        CashFlowItem(
            description = 'Wage',
            amount = int('1200'),
            date_created = date.today(),
            frequency = 'Weekly',
            user = users[1],
            category_id = 1
        ),
        CashFlowItem(
            description = 'electricity',
            amount = int('50'),
            date_created = date.today(),
            frequency = 'Weekly',
            user = users[1],
            category_id = 2
        ),
        CashFlowItem(
            description = 'Home Loan',
            amount = int('1000'),
            date_created = date.today(),
            frequency = 'Monthly',
            user = users[0],
            category_id = 2
        ),
    ]

    db.session.add_all(cash_flow_items)
    db.session.commit()

    outstanding_debts = [
        Debt(
            outstanding_amount = float('25000'),
            cash_flow_item_id = 5
        ),
        Debt(
            outstanding_amount = float('300000'),
            cash_flow_item_id = 8
        )
    ]

    db.session.add_all(outstanding_debts)
    db.session.commit()

    savings = [
        Saving(
            bank_name = 'ANZ',
            current_amount = float('5000'),
            date_updated = date.today(),
            user_id = 1
        ),
        Saving(
            bank_name = 'Commbank',
            current_amount = float('30000'),
            date_updated = date.today(),
            user_id = 1
        ),
        Saving(
            bank_name = 'ANZ',
            current_amount = float('150'),
            date_updated = date.today(),
            user_id = 2
        ),
        Saving(
            bank_name = 'Qcountry',
            current_amount = float('250000'),
            date_updated = date.today(),
            user_id = 3
        ),
        Saving(
            bank_name = 'NAB',
            current_amount = float('7500'),
            date_updated = date.today(),
            user_id = 4
        )
    ]

    db.session.add_all(savings)
    db.session.commit()
    print('Tables seeded')
