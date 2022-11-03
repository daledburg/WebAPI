from init import db, ma
from marshmallow import fields

class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    cash_flow_item = db.relationship('CashFlowItem', back_populates='budget')
    
    user = db.relationship('User', back_populates='budget')

class BudgetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id')