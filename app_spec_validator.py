class AppSpecValidator:
    def validate(self, app_spec):
        # Validate if spec is legal
        allowed_actions = ['scale_up', 'scale_down', 'restart', 'heal', 'monitor']
        if app_spec.get('action') not in allowed_actions:
            return False
        if 'target' not in app_spec:
            return False
        return True