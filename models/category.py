from init import db, ma
from marshmallow import fields

# Create Category Model to show incomes or expenses
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    is_income = db.Column(db.Boolean, default=False)
    is_expense = db.Column(db.Boolean, default=False)

    cash_flow_items = db.relationship('CashFlowItem', back_populates='category', cascade='all, delete')

# Category schema 
class CategorySchema(ma.Schema):
    cash_flow_items = fields.List(fields.Nested('CashFlowItemSchema', only=['description', 'amount', 'frequency', 'user_id', 'debt']))
    
    class Meta:
        fields = ('id', 'is_income', 'is_expense', 'cash_flow_items')
        oredered = True
