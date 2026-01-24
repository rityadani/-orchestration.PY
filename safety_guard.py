import logging

class SafetyGuard:
    def __init__(self):
        # Strict environment-based action allowlists
        self.allowlists = {
            'prod': ['monitor', 'heal', 'scale_down'],  # Conservative actions for prod
            'dev': ['monitor', 'heal', 'scale_up', 'scale_down', 'restart'],  # More flexible for dev
            'test': ['monitor', 'restart', 'scale_up', 'scale_down', 'heal']  # Full actions for test
        }
    
    def guard(self, app_spec):
        # Get environment from runtime_context or default to 'prod'
        env = app_spec.get('runtime_context', {}).get('environment', 'prod')
        allowed_actions = self.allowlists.get(env, self.allowlists['prod'])
        
        # Enforce allowlist: downgrade unsafe actions
        if app_spec.get('action') not in allowed_actions:
            logging.warning(f"Action '{app_spec['action']}' not allowed in {env}. Downgrading to 'monitor'.")
            app_spec['action'] = 'monitor'
        
        # Apply additional safety rules
        runtime = app_spec.get('runtime_context', {})
        if app_spec.get('action') == 'restart' and runtime.get('health', 0) > 0.8:
            # Don't restart healthy services
            app_spec['action'] = 'monitor'
        if app_spec.get('action') == 'scale_up' and runtime.get('health', 0) > 0.9:
            # Don't scale up if already very healthy
            app_spec['action'] = 'monitor'
        # Add more safety rules as needed
        return app_spec