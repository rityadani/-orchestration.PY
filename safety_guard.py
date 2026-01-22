class SafetyGuard:
    def guard(self, app_spec):
        # Apply safety rules
        runtime = app_spec.get('runtime_context', {})
        if app_spec.get('action') == 'restart' and runtime.get('health', 0) > 0.8:
            # Don't restart healthy services
            app_spec['action'] = 'monitor'
        if app_spec.get('action') == 'scale_up' and runtime.get('health', 0) > 0.9:
            # Don't scale up if already very healthy
            app_spec['action'] = 'monitor'
        # Add more safety rules as needed
        return app_spec