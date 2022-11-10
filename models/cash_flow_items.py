from sqlalchemy import ForeignKey
from init import db, ma
from marshmallow.validate import Length, Range, OneOf, And, Regexp
from marshmallow import fields

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
    # Listed views and nested for items when viewing cash flow schema
    user = fields.Nested('UserSchema', only=['f_name', 'id'])
    debt = fields.List(fields.Nested('DebtSchema', only=['outstanding_amount']))
    # Validate entrie for cash flow items through schema
    description = fields.String(required=True, validate=Length(min=1))
    amount = fields.Float(required=True, validate=And(
        Range(min=0.0, error='Amount must be greater than 0'),
        Regexp('^[0-9]+', error='Only numbers are allowed')))
    frequency = fields.String(load_default=VALID_FREQUENCIES[0], validate=OneOf(VALID_FREQUENCIES))
    
    class Meta:
        fields = ('id', 'description', 'amount', 'date_created', 'frequency', 'user_id', 'category_id', 'debt')
        ordered = True
