import pytest
from src.infrastructure.web.app import create_app
from src.infrastructure.database.models import db, HoneytokenDB, AlertDB
from src.domain.entities import Honeytoken
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
        db.session.add(HoneytokenDB(route="/test-json", description="JSON Trap", response_type='json'))
        db.session.add(HoneytokenDB(route="/test-html", description="HTML Trap", response_type='html'))
        db.session.add(HoneytokenDB(route="/inactive-trap", description="Inactive", is_active=False))
        db.session.commit()
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

def test_json_honeytoken_trigger(client):
    """Test standard JSON honeytoken (returns 403)"""
    response = client.get('/test-json')
    assert response.status_code == 403
    assert b"Access restricted" in response.data

def test_html_honeytoken_response(client):
    """Test the 'Deception' layer: HTML honeytoken (returns 200 + Fake UI)"""
    response = client.get('/test-html')
    assert response.status_code == 200
    assert "Infrastructure Portal" in response.data.decode()
    assert "Authentication Required" in response.data.decode()

def test_alert_persistence(client, app):
    """Verify that metadata (IP, UA) is correctly saved in DB"""
    test_ua = "Malicious-Scanner-V1"
    client.get('/test-json', environ_overrides={'HTTP_USER_AGENT': test_ua})
    
    with app.app_context():
        alert = AlertDB.query.filter_by(target_route='/test-json').first()
        assert alert is not None
        assert alert.user_agent == test_ua
        assert alert.attacker_ip == '127.0.0.1'

def test_inactive_honeytoken(client, app):
    """Ensure inactive tokens do not trigger and return 404"""
    response = client.get('/inactive-trap')
    assert response.status_code == 404
    
    with app.app_context():
        alert = AlertDB.query.filter_by(target_route='/inactive-trap').first()
        assert alert is None

def test_unknown_route(client):
    """Standard 404 for non-existent routes"""
    response = client.get('/not-a-trap-neither-a-real-route')
    assert response.status_code == 404
