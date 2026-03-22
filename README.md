# 🛡️ Honeytoken Intrusion Detection Microservice (Flask)

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-brightgreen)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance **Cybersecurity Tripwire** designed to detect and alert against reconnaissance attempts. This microservice implements **Honeytokens** (synthetic decoy endpoints) that trigger real-time alerts when touched by a malicious actor.

## 🚀 Key Value Proposition
- **Early Reconnaissance Detection**: Identifies attackers during their first scan, before they find a real vulnerability.
- **High-Fidelity Signal**: No legitimate user should ever access `/admin/config-backup` or `/.env`. Any trigger is a near-certain intrusion attempt.
- **Zero Latency Alerting**: Immediate notifications via **Discord/Slack Webhooks**.
- **Stealth Monitoring**: Attackers are misled by standard 403/404 responses while their metadata (IP, Headers, User-Agent) is logged.

---

## 🏗️ Clean Architecture
Designed with separation of concerns to ensure scalability and testability:

- **`src/domain`**: Business entities and repository interfaces. Pure Python logic.
- **`src/application`**: Domain-driven use cases (`TriggerAlertUseCase`).
- **`src/infrastructure`**: 
  - **Web**: Global Flask Middleware for stealthy interception.
  - **Database**: Repository implementation with SQLAlchemy (SQLite/PostgreSQL compatible).
  - **Services**: External Adapters for Discord/Slack notifications.

---

## 🛠️ Performance & Scalability
- **Middleware Interception**: Custom hooks in Flask's `before_request` for global coverage.
- **Optimized Lookups**: Uses indexed route lookups in the database for minimal overhead on legitimate traffic.
- **Persistence**: Event-driven alert logging for audit trails.

---

## 🚦 Getting Started

### 1. Prerequisites
- Python 3.8+
- Discord/Slack Webhook URL

### 2. Installation
```powershell
# Clone the repository
git clone https://github.com/youruser/honeytoken_intruder.git
cd honeytoken_intruder

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Rename/Create a `.env` file in the root directory:
```env
# CRITICAL: Do not commit your real .env to version control
DATABASE_URL=sqlite:///honeytoken.db
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-id/your-token
PORT=5000
DEBUG=True
```

### 4. Running the App
```powershell
python main.py
```

### 5. Simulate an Attack (Validation)
Use the included testing script to verify the trap:
```powershell
python test_client_attack.py
```

---

## 🧪 Testing Suite
Comprehensive test coverage using **Pytest**:
```powershell
python -m pytest
```

## 🔒 Security Disclaimer
This project is for educational and defensive purposes. Ensure you have authorization before deploying security tooling in production environments.

---
**Developed by [Your Name]** - *Expertise in Python, Backend Architecture and Cybersecurity.*
