import pytest
from flask import json
from app.models.farm import Farm

def test_get_farms_empty(client):
    response = client.get('/api/farms/')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []

def test_create_farm(client):
    response = client.post('/api/farms/', json={'name': 'New Farm'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'New Farm'
    assert 'id' in data

def test_create_farm_duplicate(client):
    client.post('/api/farms/', json={'name': 'Farm 1'})
    response = client.post('/api/farms/', json={'name': 'Farm 1'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'Validation error' in data['message']
    assert 'name' in data['errors']

def test_create_farm_empty_name(client):
    response = client.post('/api/farms/', json={'name': ''})
    assert response.status_code == 400

def test_get_farm_by_id(client):
    create_response = client.post('/api/farms/', json={'name': 'Test Farm'})
    farm_id = create_response.get_json()['id']
    
    response = client.get(f'/api/farms/{farm_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Test Farm'

def test_get_farm_not_found(client):
    response = client.get('/api/farms/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Farm not found'

def test_update_farm(client):
    create_response = client.post('/api/farms/', json={'name': 'Old Name'})
    farm_id = create_response.get_json()['id']
    
    response = client.put(f'/api/farms/{farm_id}', json={'name': 'New Name'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'New Name'

def test_update_farm_duplicate(client):
    client.post('/api/farms/', json={'name': 'Farm A'})
    response = client.post('/api/farms/', json={'name': 'Farm B'})
    farm_id = response.get_json()['id']
    
    response = client.put(f'/api/farms/{farm_id}', json={'name': 'Farm A'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'name' in data['errors']

def test_delete_farm(client):
    create_response = client.post('/api/farms/', json={'name': 'To Delete'})
    farm_id = create_response.get_json()['id']
    
    response = client.delete(f'/api/farms/{farm_id}')
    assert response.status_code == 204
    
    response = client.get(f'/api/farms/{farm_id}')
    assert response.status_code == 404

def test_delete_farm_with_records(client, app):
    # Create farm
    create_response = client.post('/api/farms/', json={'name': 'Farm With Records'})
    farm_id = create_response.get_json()['id']
    
    # Create record for this farm
    client.post('/api/reproduction-records/', json={
        'farm_id': farm_id,
        'date': '2026-06-28'
    })
    
    # Try to delete farm
    response = client.delete(f'/api/farms/{farm_id}')
    assert response.status_code == 400
    data = response.get_json()
    assert 'Farm has existing reproduction records' in data['message']