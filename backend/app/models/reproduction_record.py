from datetime import datetime
from app.extensions import db
from sqlalchemy import CheckConstraint, UniqueConstraint

class ReproductionRecord(db.Model):
    __tablename__ = 'reproduction_records'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    abort = db.Column(db.Integer, default=0)
    bulls_from_cows = db.Column(db.Integer, default=0)
    bulls_from_heifers = db.Column(db.Integer, default=0)
    conception_cows = db.Column(db.Integer, default=0)
    conception_heifers = db.Column(db.Integer, default=0)
    cows_from_cows = db.Column(db.Integer, default=0)
    cows_from_heifers = db.Column(db.Integer, default=0)
    dead_bulls = db.Column(db.Integer, default=0)
    dead_heifers = db.Column(db.Integer, default=0)
    preg_rate_cows = db.Column(db.Float, default=0.0)
    preg_rate_heifers = db.Column(db.Float, default=0.0)
    reproduction_cows = db.Column(db.Integer, default=0)
    reproduction_heifers = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint('abort >= 0', name='check_abort_non_negative'),
        CheckConstraint('bulls_from_cows >= 0', name='check_bulls_from_cows_non_negative'),
        CheckConstraint('bulls_from_heifers >= 0', name='check_bulls_from_heifers_non_negative'),
        CheckConstraint('conception_cows >= 0', name='check_conception_cows_non_negative'),
        CheckConstraint('conception_heifers >= 0', name='check_conception_heifers_non_negative'),
        CheckConstraint('cows_from_cows >= 0', name='check_cows_from_cows_non_negative'),
        CheckConstraint('cows_from_heifers >= 0', name='check_cows_from_heifers_non_negative'),
        CheckConstraint('dead_bulls >= 0', name='check_dead_bulls_non_negative'),
        CheckConstraint('dead_heifers >= 0', name='check_dead_heifers_non_negative'),
        CheckConstraint('preg_rate_cows >= 0 AND preg_rate_cows <= 100', name='check_preg_rate_cows_range'),
        CheckConstraint('preg_rate_heifers >= 0 AND preg_rate_heifers <= 100', name='check_preg_rate_heifers_range'),
        CheckConstraint('reproduction_cows >= 0', name='check_reproduction_cows_non_negative'),
        CheckConstraint('reproduction_heifers >= 0', name='check_reproduction_heifers_non_negative'),
        UniqueConstraint('farm_id', 'date', name='unique_farm_date')
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'farm_name': self.farm.name if self.farm else None,
            'date': self.date.isoformat() if self.date else None,
            'abort': self.abort,
            'bulls_from_cows': self.bulls_from_cows,
            'bulls_from_heifers': self.bulls_from_heifers,
            'conception_cows': self.conception_cows,
            'conception_heifers': self.conception_heifers,
            'cows_from_cows': self.cows_from_cows,
            'cows_from_heifers': self.cows_from_heifers,
            'dead_bulls': self.dead_bulls,
            'dead_heifers': self.dead_heifers,
            'preg_rate_cows': self.preg_rate_cows,
            'preg_rate_heifers': self.preg_rate_heifers,
            'reproduction_cows': self.reproduction_cows,
            'reproduction_heifers': self.reproduction_heifers,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }