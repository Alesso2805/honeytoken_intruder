import pytest
from src.infrastructure.web.app import create_app
from src.infrastructure.database.models import db
from unittest.mock import MagicMock

@pytest.fixture
def app():
    """Create a Flask test application"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    """Test standard API route (should not trigger alerts)"""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert b"healthy" in response.data

def test_honeytoken_trigger(client, monkeypatch):
    """Test a high-signal honeytoken trap"""
    
    mock_sender = MagicMock()
    
    response = client.get('/admin/config-backup')
    
    assert response.status_code == 403
    assert b"Access restricted" in response.data

def test_unknown_route(client):
    """Wait, unknown routes should return 404 naturally unless they are tokens"""
    response = client.get('/not-a-trap-neither-a-real-route')
    assert response.status_code == 404
