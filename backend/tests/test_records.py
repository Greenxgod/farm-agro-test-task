import pytest
from flask import json
from datetime import datetime, timedelta

def test_create_record(client, test_farm):
    response = client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-28',
        'abort': 5,
        'bulls_from_cows': 10,
        'preg_rate_cows': 75.5
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['farm_id'] == test_farm.id
    assert data['abort'] == 5
    assert data['preg_rate_cows'] == 75.5

def test_create_record_negative_value(client, test_farm):
    response = client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-28',
        'abort': -5
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'Validation error' in data['message']

def test_create_record_preg_rate_out_of_range(client, test_farm):
    response = client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-28',
        'preg_rate_cows': 150
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'Validation error' in data['message']

def test_create_record_duplicate(client, test_farm):
    # First record
    client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-28'
    })
    
    # Duplicate
    response = client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-28'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'already exists' in str(data['errors'])

def test_create_record_future_date(client, test_farm):
    future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
    response = client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': future_date
    })
    assert response.status_code == 400

def test_get_records_with_filters(client, test_farm):
    # Create multiple records
    client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-01'
    })
    client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-15'
    })
    client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-30'
    })
    
    response = client.get('/api/reproduction-records/?date_from=2026-06-10&date_to=2026-06-20')
    assert response.status_code == 200
    data = response.get_json()
    assert data['pagination']['total'] == 1

def test_get_records_pagination(client, test_farm):
    for i in range(25):
        client.post('/api/reproduction-records/', json={
            'farm_id': test_farm.id,
            'date': f'2026-06-{(i+1):02d}'
        })
    
    response = client.get('/api/reproduction-records/?page=1&limit=10')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 10
    assert data['pagination']['total'] == 25
    assert data['pagination']['pages'] == 3

def test_get_record_by_id(client, test_farm):
    create_response = client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-28',
        'abort': 10
    })
    record_id = create_response.get_json()['id']
    
    response = client.get(f'/api/reproduction-records/{record_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == record_id
    assert data['abort'] == 10

def test_get_record_not_found(client):
    response = client.get('/api/reproduction-records/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Record not found'

def test_update_record(client, test_farm):
    create_response = client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-28',
        'abort': 5
    })
    record_id = create_response.get_json()['id']
    
    response = client.put(f'/api/reproduction-records/{record_id}', json={
        'abort': 10,
        'preg_rate_cows': 85.5
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['abort'] == 10
    assert data['preg_rate_cows'] == 85.5

def test_delete_record(client, test_farm):
    create_response = client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-28'
    })
    record_id = create_response.get_json()['id']
    
    response = client.delete(f'/api/reproduction-records/{record_id}')
    assert response.status_code == 204
    
    response = client.get(f'/api/reproduction-records/{record_id}')
    assert response.status_code == 404

def test_statistics_basic(client, test_farm):
    client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-01',
        'abort': 2,
        'dead_bulls': 1,
        'preg_rate_cows': 50
    })
    client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-02',
        'abort': 3,
        'dead_bulls': 2,
        'preg_rate_cows': 70
    })
    
    response = client.get('/api/reproduction-records/statistics')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_records'] == 2
    assert data['total_abort'] == 5
    assert data['total_dead_bulls'] == 3
    assert data['avg_preg_rate_cows'] == 60.0

def test_statistics_with_filters(client, test_farm):
    # Create another farm
    farm2_response = client.post('/api/farms/', json={'name': 'Farm 2'})
    farm2_id = farm2_response.get_json()['id']
    
    client.post('/api/reproduction-records/', json={
        'farm_id': test_farm.id,
        'date': '2026-06-01',
        'abort': 10
    })
    client.post('/api/reproduction-records/', json={
        'farm_id': farm2_id,
        'date': '2026-06-01',
        'abort': 20
    })
    
    response = client.get(f'/api/reproduction-records/statistics?farm_id={test_farm.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_records'] == 1
    assert data['total_abort'] == 10

def test_statistics_empty(client):
    response = client.get('/api/reproduction-records/statistics')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_records'] == 0
    assert data['total_abort'] == 0
    assert data['avg_preg_rate_cows'] == 0