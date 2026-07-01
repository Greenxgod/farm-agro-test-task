import pytest
from app.models.farm import Farm
from app.models.reproduction_record import ReproductionRecord
from app.extensions import db
from sqlalchemy.exc import IntegrityError

def test_farm_name_required(app, db_session):
    farm = Farm(name=None)
    db_session.add(farm)
    with pytest.raises(Exception):
        db_session.commit()

def test_farm_name_unique(app, db_session):
    farm1 = Farm(name='Unique Farm')
    db_session.add(farm1)
    db_session.commit()
    
    farm2 = Farm(name='Unique Farm')
    db_session.add(farm2)
    with pytest.raises(Exception):
        db_session.commit()

def test_record_farm_id_required(app, db_session, test_farm):
    record = ReproductionRecord(
        farm_id=None,
        date='2026-06-28'
    )
    db_session.add(record)
    with pytest.raises(Exception):
        db_session.commit()

def test_record_date_required(app, db_session, test_farm):
    record = ReproductionRecord(
        farm_id=test_farm.id,
        date=None
    )
    db_session.add(record)
    with pytest.raises(Exception):
        db_session.commit()

def test_record_negative_abort(app, db_session, test_farm):
    record = ReproductionRecord(
        farm_id=test_farm.id,
        date='2026-06-28',
        abort=-1
    )
    db_session.add(record)
    with pytest.raises(Exception):
        db_session.commit()

def test_record_preg_rate_out_of_range(app, db_session, test_farm):
    record = ReproductionRecord(
        farm_id=test_farm.id,
        date='2026-06-28',
        preg_rate_cows=150
    )
    db_session.add(record)
    with pytest.raises(Exception):
        db_session.commit()

def test_record_unique_farm_date(app, db_session, test_farm):
    record1 = ReproductionRecord(
        farm_id=test_farm.id,
        date='2026-06-28'
    )
    db_session.add(record1)
    db_session.commit()
    
    record2 = ReproductionRecord(
        farm_id=test_farm.id,
        date='2026-06-28'
    )
    db_session.add(record2)
    with pytest.raises(Exception):
        db_session.commit()