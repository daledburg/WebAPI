from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date)

    budget = db.relationship('Budget', back_populates='user')
    cash_flow_item = db.relationship('CashFlowItem', back_populates='user')


class UserSchema(ma.Schema):
    cash_flow_item = fields.List(fields.Nested('CashFlowItemSchema', only=['description', 'amount']))
    # budgets = fields.List('BudgetSchema', exclude=['user'])
    class Meta:
        fields = ('id', 'f_name', 'l_name', 'email', 'password', 'date_created', 'cash_flow_item')

