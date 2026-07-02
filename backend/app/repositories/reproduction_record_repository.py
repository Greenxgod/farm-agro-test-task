from sqlalchemy import and_, or_
from app.models.reproduction_record import ReproductionRecord
from app.models.farm import Farm
from app.extensions import db

class ReproductionRecordRepository:
    @staticmethod
    def get_all(filters=None, sort=None, order='asc', page=1, limit=20):
        query = db.session.query(ReproductionRecord).join(Farm)
        
        if filters:
            if filters.get('farm_id'):
                query = query.filter(ReproductionRecord.farm_id == filters['farm_id'])
            
            if filters.get('date_from'):
                query = query.filter(ReproductionRecord.date >= filters['date_from'])
            
            if filters.get('date_to'):
                query = query.filter(ReproductionRecord.date <= filters['date_to'])
        
        if sort:
            if sort == 'date':
                order_by = ReproductionRecord.date
            elif sort == 'farm_name':
                order_by = Farm.name
            else:
                order_by = ReproductionRecord.id
            
            if order == 'desc':
                query = query.order_by(order_by.desc())
            else:
                query = query.order_by(order_by.asc())
        else:
            query = query.order_by(ReproductionRecord.date.desc())
        
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit
        }
    
    @staticmethod
    def get_by_id(record_id):
        return ReproductionRecord.query.get(record_id)
    
    @staticmethod
    def create(data):
        record = ReproductionRecord(**data)
        db.session.add(record)
        db.session.commit()
        return record
    
    @staticmethod
    def update(record, data):
        for key, value in data.items():
            setattr(record, key, value)
        db.session.commit()
        return record
    
    @staticmethod
    def delete(record):
        db.session.delete(record)
        db.session.commit()
    
    @staticmethod
    def get_statistics(filters=None):
        query = db.session.query(ReproductionRecord)
        
        if filters:
            if filters.get('farm_id'):
                query = query.filter(ReproductionRecord.farm_id == filters['farm_id'])
            
            if filters.get('date_from'):
                query = query.filter(ReproductionRecord.date >= filters['date_from'])
            
            if filters.get('date_to'):
                query = query.filter(ReproductionRecord.date <= filters['date_to'])
        
        records = query.all()
        
        if not records:
            return {
                'total_records': 0,
                'total_abort': 0,
                'total_dead_bulls': 0,
                'total_dead_heifers': 0,
                'avg_preg_rate_cows': 0,
                'avg_preg_rate_heifers': 0,
                'total_bulls_from_cows': 0,
                'total_bulls_from_heifers': 0,
                'total_cows_from_cows': 0,
                'total_cows_from_heifers': 0
            }
        
        return {
            'total_records': len(records),
            'total_abort': sum(r.abort for r in records),
            'total_dead_bulls': sum(r.dead_bulls for r in records),
            'total_dead_heifers': sum(r.dead_heifers for r in records),
            'avg_preg_rate_cows': round(sum(r.preg_rate_cows for r in records) / len(records), 2),
            'avg_preg_rate_heifers': round(sum(r.preg_rate_heifers for r in records) / len(records), 2),
            'total_bulls_from_cows': sum(r.bulls_from_cows for r in records),
            'total_bulls_from_heifers': sum(r.bulls_from_heifers for r in records),
            'total_cows_from_cows': sum(r.cows_from_cows for r in records),
            'total_cows_from_heifers': sum(r.cows_from_heifers for r in records)
        }