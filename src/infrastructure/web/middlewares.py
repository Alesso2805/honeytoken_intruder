from flask import request, current_app, render_template
from ...application.alert_use_case import TriggerAlertUseCase
from ...domain.repositories import HoneytokenRepository

def setup_honeytoken_middleware(app, honeytoken_repo: HoneytokenRepository, alert_use_case: TriggerAlertUseCase):
    @app.before_request
    def intercept_honeytokens():
        """Global interceptor for decoy honeytoken endpoints"""
        
        path = request.path
        honeytoken = honeytoken_repo.find_by_route(path)
        
        if honeytoken and honeytoken.is_active:
            headers_dict = dict(request.headers)
            attacker_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            user_agent = request.headers.get('User-Agent', 'Unknown')
            
            alert_use_case.execute(
                route=path,
                ip=attacker_ip,
                user_agent=user_agent,
                headers=headers_dict
            )
            
            if honeytoken.response_type == 'html':
                return render_template('fake_login.html'), 200
            
            return {"message": "Access restricted"}, 403
