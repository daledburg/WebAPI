from sqlalchemy import ForeignKey
from init import db, ma
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow import fields, Schema

VALID_FREQUENCIES = ('Weekly', 'Fortnightly', 'Monthly', 'Semi-annually', 'Annually')

class CashFlowItem(db.Model):
    __tablename__ = 'cash_flow_items'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.Date)
    frequency = db.Column(db.String, default=VALID_FREQUENCIES[0])

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    debt = db.relationship('Debt', back_populates='cash_flow_item')
    user = db.relationship('User', back_populates='cash_flow_item')
    category = db.relationship('Category', back_populates='cash_flow_items')


class CashFlowItemSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['f_name', 'id'])
    debt = fields.List(fields.Nested('DebtSchema', only=['outstanding_amount']))
    
    class Meta:
        fields = ('id', 'description', 'amount', 'date_created', 'frequency', 'user_id', 'category_id', 'debt')
        ordered = True
