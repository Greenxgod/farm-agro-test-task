from app.models.farm import Farm
from app.extensions import db

class FarmRepository:
    @staticmethod
    def get_all():
        return Farm.query.order_by(Farm.name).all()
    
    @staticmethod
    def get_by_id(farm_id):
        return Farm.query.get(farm_id)
    
    @staticmethod
    def create(name):
        farm = Farm(name=name)
        db.session.add(farm)
        db.session.commit()
        return farm
    
    @staticmethod
    def update(farm, name):
        farm.name = name
        db.session.commit()
        return farm
    
    @staticmethod
    def delete(farm):
        # При удалении фермы, все связанные записи удаляются через ON DELETE CASCADE
        db.session.delete(farm)
        db.session.commit()