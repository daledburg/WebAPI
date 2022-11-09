from init import db, ma
from marshmallow import fields

class Debt(db.Model):
    __tablename__ = 'debts'

    id = db.Column(db.Integer, primary_key=True)
    outstanding_amount = db.Column(db.Float, nullable=False)

    cash_flow_item_id = db.Column(db.Integer, db.ForeignKey('cash_flow_items.id'), nullable=False)

    cash_flow_item = db.relationship('CashFlowItem', back_populates='debt', cascade='all, delete')

class DebtSchema(ma.Schema):
    cash_flow_item = fields.Nested('CashFlowItemSchema')

    class Meta:
        fields = ('id', 'outstanding_amount', 'final_payment_date', 'cash_flow_item_id')
        ordered = True
