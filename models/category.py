from init import db, ma
from marshmallow import fields

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    is_income = db.Column(db.Boolean, default=False)
    is_expense = db.Column(db.Boolean, default=False)
    is_outstanding_debt = db.Column(db.Boolean, default=False)

    cash_flow_item_id = db.Column(db.Integer, db.ForeignKey('cash_flow_items.id'), nullable=False)

    cash_flow_item = db.relationship('CashFlowItem', back_populates='category')

class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'is_income', 'is_outstanding_debt', 'is_expense')