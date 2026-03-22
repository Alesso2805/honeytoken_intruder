from flask import Flask, jsonify
from ..database.models import db
from ..database.repositories_impl import SQLAlchemyAlertRepository, SQLAlchemyHoneytokenRepository
from ..services.notification_service import NotificationService
from ...application.alert_use_case import TriggerAlertUseCase
from .middlewares import setup_honeytoken_middleware
from ...domain.entities import Honeytoken
import os

def create_app(config_name=None):
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///honeytoken.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    alert_repo = SQLAlchemyAlertRepository()
    honeytoken_repo = SQLAlchemyHoneytokenRepository()
    notification_service = NotificationService(os.getenv('DISCORD_WEBHOOK_URL', ''))
    
    alert_use_case = TriggerAlertUseCase(alert_repo, notification_service)
    
    setup_honeytoken_middleware(app, honeytoken_repo, alert_use_case)
    
    @app.route('/api/v1/health')
    def health_check():
        return jsonify({"status": "healthy", "service": "honeytoken-detector"}), 200

    @app.route('/api/v1/honeytokens', methods=['GET'])
    def list_tokens():
        tokens = honeytoken_repo.find_all()
        return jsonify([{"route": t.route, "description": t.description} for t in tokens]), 200

    with app.app_context():
        db.create_all()
        if not honeytoken_repo.find_all():
             honeytoken_repo.save(Honeytoken(route="/admin/config-backup", description="Mock Sensitive Backup"))
             honeytoken_repo.save(Honeytoken(route="/.env", description="Secret Environment Variables"))
             honeytoken_repo.save(Honeytoken(route="/wp-admin", description="WordPress Mock login"))

    return app
