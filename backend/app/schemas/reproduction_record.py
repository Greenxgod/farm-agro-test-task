from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime
from app.models.reproduction_record import ReproductionRecord

class ReproductionRecordSchema(Schema):
    id = fields.Int(dump_only=True)
    farm_id = fields.Int(required=True, validate=validate.Range(min=1))
    date = fields.Date(required=True)
    abort = fields.Int(missing=0, validate=validate.Range(min=0))
    bulls_from_cows = fields.Int(missing=0, validate=validate.Range(min=0))
    bulls_from_heifers = fields.Int(missing=0, validate=validate.Range(min=0))
    conception_cows = fields.Int(missing=0, validate=validate.Range(min=0))
    conception_heifers = fields.Int(missing=0, validate=validate.Range(min=0))
    cows_from_cows = fields.Int(missing=0, validate=validate.Range(min=0))
    cows_from_heifers = fields.Int(missing=0, validate=validate.Range(min=0))
    dead_bulls = fields.Int(missing=0, validate=validate.Range(min=0))
    dead_heifers = fields.Int(missing=0, validate=validate.Range(min=0))
    preg_rate_cows = fields.Float(missing=0.0, validate=validate.Range(min=0, max=100))
    preg_rate_heifers = fields.Float(missing=0.0, validate=validate.Range(min=0, max=100))
    reproduction_cows = fields.Int(missing=0, validate=validate.Range(min=0))
    reproduction_heifers = fields.Int(missing=0, validate=validate.Range(min=0))
    farm_name = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('date')
    def validate_date(self, value):
        if value and value > datetime.now().date():
            raise ValidationError('Date cannot be in the future')
    
    @validates('farm_id')
    def validate_farm_id(self, value):
        from app.models.farm import Farm
        if not Farm.query.get(value):
            raise ValidationError('Farm does not exist')

class ReproductionRecordCreateSchema(Schema):
    farm_id = fields.Int(required=True, validate=validate.Range(min=1))
    date = fields.Date(required=True)
    abort = fields.Int(missing=0, validate=validate.Range(min=0))
    bulls_from_cows = fields.Int(missing=0, validate=validate.Range(min=0))
    bulls_from_heifers = fields.Int(missing=0, validate=validate.Range(min=0))
    conception_cows = fields.Int(missing=0, validate=validate.Range(min=0))
    conception_heifers = fields.Int(missing=0, validate=validate.Range(min=0))
    cows_from_cows = fields.Int(missing=0, validate=validate.Range(min=0))
    cows_from_heifers = fields.Int(missing=0, validate=validate.Range(min=0))
    dead_bulls = fields.Int(missing=0, validate=validate.Range(min=0))
    dead_heifers = fields.Int(missing=0, validate=validate.Range(min=0))
    preg_rate_cows = fields.Float(missing=0.0, validate=validate.Range(min=0, max=100))
    preg_rate_heifers = fields.Float(missing=0.0, validate=validate.Range(min=0, max=100))
    reproduction_cows = fields.Int(missing=0, validate=validate.Range(min=0))
    reproduction_heifers = fields.Int(missing=0, validate=validate.Range(min=0))
    
    @validates('date')
    def validate_date(self, value):
        if value and value > datetime.now().date():
            raise ValidationError('Date cannot be in the future')
    
    @validates('farm_id')
    def validate_farm_id(self, value):
        from app.models.farm import Farm
        if not Farm.query.get(value):
            raise ValidationError('Farm does not exist')