from datetime import datetime
from app.repositories.reproduction_record_repository import ReproductionRecordRepository
from app.models.reproduction_record import ReproductionRecord
from app.errors import AppError

class ReproductionRecordService:
    @staticmethod
    def get_records(farm_id=None, date_from=None, date_to=None, sort=None, order='asc', page=1, limit=20):
        filters = {}
        if farm_id:
            filters['farm_id'] = farm_id
        if date_from:
            filters['date_from'] = datetime.strptime(date_from, '%Y-%m-%d').date()
        if date_to:
            filters['date_to'] = datetime.strptime(date_to, '%Y-%m-%d').date()
        
        result = ReproductionRecordRepository.get_all(filters, sort, order, page, limit)
        return {
            'items': [record.to_dict() for record in result['items']],
            'pagination': {
                'page': result['page'],
                'limit': result['limit'],
                'total': result['total'],
                'pages': result['pages']
            }
        }
    
    @staticmethod
    def get_record_by_id(record_id):
        record = ReproductionRecordRepository.get_by_id(record_id)
        if not record:
            raise AppError('Record not found', 404)
        return record
    
    @staticmethod
    def create_record(data):
        # Check for duplicate farm+date
        existing = ReproductionRecord.query.filter_by(
            farm_id=data['farm_id'],
            date=data['date']
        ).first()
        
        if existing:
            raise AppError(
                'Validation error',
                400,
                {'date': ['Record for this farm and date already exists']}
            )
        
        return ReproductionRecordRepository.create(data)
    
    @staticmethod
    def update_record(record_id, data):
        record = ReproductionRecordService.get_record_by_id(record_id)
        
        # Check for duplicate farm+date if farm_id or date changed
        if 'farm_id' in data or 'date' in data:
            farm_id = data.get('farm_id', record.farm_id)
            date = data.get('date', record.date)
            
            existing = ReproductionRecord.query.filter_by(
                farm_id=farm_id,
                date=date
            ).first()
            
            if existing and existing.id != record_id:
                raise AppError(
                    'Validation error',
                    400,
                    {'date': ['Record for this farm and date already exists']}
                )
        
        return ReproductionRecordRepository.update(record, data)
    
    @staticmethod
    def delete_record(record_id):
        record = ReproductionRecordService.get_record_by_id(record_id)
        ReproductionRecordRepository.delete(record)
    
    @staticmethod
    def get_statistics(farm_id=None, date_from=None, date_to=None):
        filters = {}
        if farm_id:
            filters['farm_id'] = farm_id
        if date_from:
            filters['date_from'] = datetime.strptime(date_from, '%Y-%m-%d').date()
        if date_to:
            filters['date_to'] = datetime.strptime(date_to, '%Y-%m-%d').date()
        
        return ReproductionRecordRepository.get_statistics(filters)