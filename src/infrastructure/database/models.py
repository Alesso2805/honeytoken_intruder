from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ...domain.entities import Alert, Honeytoken

db = SQLAlchemy()

class HoneytokenDB(db.Model):
    __tablename__ = 'honeytokens'
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    response_type = db.Column(db.String(50), default='json')

class AlertDB(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    target_route = db.Column(db.String(255), nullable=False)
    attacker_ip = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.Text, nullable=False)
    headers = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
