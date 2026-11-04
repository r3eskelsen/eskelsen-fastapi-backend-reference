from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.main import app, Base, get_db
import pytest

@pytest.fixture
def client():
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    def override():
        with Session(engine) as db:
            yield db
    app.dependency_overrides[get_db] = override
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()

def test_health(client):
    assert client.get('/health').json() == {'status': 'ok'}

def test_create_and_read_item(client):
    created = client.post('/items', json={'name': 'Demo Widget', 'category': 'test', 'quantity': 3})
    assert created.status_code == 201
    item_id = created.json()['id']
    assert client.get(f'/items/{item_id}').json()['name'] == 'Demo Widget'
    assert len(client.get('/items').json()) == 1

def test_invalid_quantity(client):
    assert client.post('/items', json={'name': 'A', 'category': 'test', 'quantity': -1}).status_code == 422

def test_missing_item(client):
    assert client.get('/items/999').status_code == 404

def test_delete_item(client):
    item_id = client.post('/items', json={'name': 'A', 'category': 'test', 'quantity': 0}).json()['id']
    assert client.delete(f'/items/{item_id}').status_code == 204
    assert client.get(f'/items/{item_id}').status_code == 404

def test_invalid_limit(client):
    assert client.get('/items?limit=101').status_code == 422
