from app.repositories.farm_repository import FarmRepository
from app.errors import AppError

class FarmService:
    @staticmethod
    def get_all_farms():
        return FarmRepository.get_all()
    
    @staticmethod
    def get_farm_by_id(farm_id):
        farm = FarmRepository.get_by_id(farm_id)
        if not farm:
            raise AppError('Farm not found', 404)
        return farm
    
    @staticmethod
    def create_farm(name):
        # Check if farm with this name exists
        existing = FarmRepository.get_all()
        for farm in existing:
            if farm.name.lower() == name.lower():
                raise AppError('Validation error', 400, {'name': ['Farm with this name already exists']})
        
        return FarmRepository.create(name)
    
    @staticmethod
    def update_farm(farm_id, name):
        farm = FarmService.get_farm_by_id(farm_id)
        
        # Check if another farm has this name
        existing = FarmRepository.get_all()
        for f in existing:
            if f.id != farm_id and f.name.lower() == name.lower():
                raise AppError('Validation error', 400, {'name': ['Farm with this name already exists']})
        
        return FarmRepository.update(farm, name)
    
    @staticmethod
    def delete_farm(farm_id):
        farm = FarmService.get_farm_by_id(farm_id)
        
        # Check if farm has records
        if farm.records:
            raise AppError(
                'Cannot delete farm with existing records',
                400,
                {'farm_id': ['Farm has existing reproduction records. Delete them first.']}
            )
        
        FarmRepository.delete(farm)