from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date)

    cash_flow_item = db.relationship('CashFlowItem', back_populates='user', cascade='all, delete')
    saving = db.relationship('Saving', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    cash_flow_item = fields.List(fields.Nested('CashFlowItemSchema', only=['description', 'amount']))
    saving = fields.List(fields.Nested('SavingSchema', only=['bank_name', 'current_amount', 'date_updated']))
    class Meta:
        fields = ('id', 'f_name', 'l_name', 'email', 'password', 'date_created', 'cash_flow_item', 'saving')
        ordered = True
