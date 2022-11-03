from sqlalchemy import ForeignKey
from init import db, ma
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow import fields

VALID_FREQUENCIES = ('Weekly', 'Fortnightly', 'Monthly', 'Semi-annually', 'Annually')

class CashFlowItem(db.Model):
    __tablename__ = 'cash_flow_items'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.Date)
    frequency = db.Column(db.String, default=VALID_FREQUENCIES[0])

    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    category = db.relationship('Category', back_populates='cash_flow_item')
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    user = db.relationship('User', back_populates='cash_flow_item')
    budget = db.relationship('Budget', back_populates='cash_flow_item')


class CashFlowItemSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['f_name', 'id'])
    category = fields.List(fields.Nested('CategorySchema'))
    class Meta:
        fields = ('id', 'description', 'amount', 'date_created', 'frequency', 'user', 'category')