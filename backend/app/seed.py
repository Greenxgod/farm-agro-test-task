import random
from datetime import datetime, timedelta
from app.extensions import db
from app.models.farm import Farm
from app.models.reproduction_record import ReproductionRecord

def seed_database():
    """Seed the database with test data"""
    print("Seeding database...")
    
    # Create farms
    farms_data = [
        "Ферма 1",
        "Ферма 2", 
        "Ферма 3",
        "Ферма 4",
        "Ферма 5"
    ]
    
    farms = []
    for name in farms_data:
        farm = Farm(name=name)
        db.session.add(farm)
        farms.append(farm)
    
    db.session.commit()
    print(f"Created {len(farms)} farms")
    
    # Create reproduction records
    start_date = datetime.now().date() - timedelta(days=365)
    
    for farm in farms:
        for i in range(30):  # 30 records per farm
            date = start_date + timedelta(days=i * 12)  # Every 12 days
            
            record = ReproductionRecord(
                farm_id=farm.id,
                date=date,
                abort=random.randint(0, 5),
                bulls_from_cows=random.randint(0, 10),
                bulls_from_heifers=random.randint(0, 8),
                conception_cows=random.randint(0, 15),
                conception_heifers=random.randint(0, 12),
                cows_from_cows=random.randint(0, 20),
                cows_from_heifers=random.randint(0, 15),
                dead_bulls=random.randint(0, 5),
                dead_heifers=random.randint(0, 5),
                preg_rate_cows=round(random.uniform(20, 90), 2),
                preg_rate_heifers=round(random.uniform(20, 90), 2),
                reproduction_cows=random.randint(0, 30),
                reproduction_heifers=random.randint(0, 25)
            )
            db.session.add(record)
    
    db.session.commit()
    print(f"Created {len(farms) * 30} reproduction records")
    print("Seeding completed!")

if __name__ == '__main__':
    seed_database()