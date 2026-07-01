from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.farm import Farm

class FarmSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('name')
    def validate_name(self, value):
        if Farm.query.filter_by(name=value).first():
            raise ValidationError('Farm with this name already exists')

class FarmCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    
    @validates('name')
    def validate_name(self, value):
        if Farm.query.filter_by(name=value).first():
            raise ValidationError('Farm with this name already exists')

class FarmUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=100))
    
    @validates('name')
    def validate_name(self, value):
        if Farm.query.filter_by(name=value).first():
            raise ValidationError('Farm with this name already exists')