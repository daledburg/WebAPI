from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp, Email

# Create Model for User
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), default='')
    l_name = db.Column(db.String(50), default='')
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date)

    cash_flow_item = db.relationship('CashFlowItem', back_populates='user', cascade='all, delete')
    saving = db.relationship('Saving', back_populates='user', cascade='all, delete')

# Create Schema for users
class UserSchema(ma.Schema):
    # Create listed view for items in users
    cash_flow_item = fields.List(fields.Nested('CashFlowItemSchema', only=['description', 'amount']))
    saving = fields.List(fields.Nested('SavingSchema', only=['bank_name', 'current_amount', 'date_updated']))
    # Validate entries through User Schema
    password = fields.String(validate=Length(min=5, error='Password must be atleast 5 characters long'))
    f_name = fields.String(validate=Regexp('^[a-zA-Z0-9 ]+', error='Only letters, numbers and spaces are allowable'))
    l_name = fields.String(validate=Regexp('^[a-zA-Z0-9 ]+', error='Only letters, numbers and spaces are allowable'))
    email = fields.String(validate=Email(error='Not valid email address'))

    class Meta:
        fields = ('id', 'f_name', 'l_name', 'email', 'password', 'date_created', 'cash_flow_item', 'saving')
        ordered = True
