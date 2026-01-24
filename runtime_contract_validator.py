class RuntimeContractValidator:
    def validate(self, runtime_data):
        # Check if runtime_data has required fields
        required_fields = ['latency', 'health', 'failures', 'services']
        for field in required_fields:
            if field not in runtime_data:
                return False, "Missing required field: " + field
        
        # Additional validation for invalid states
        if not isinstance(runtime_data['latency'], (int, float)) or runtime_data['latency'] < 0:
            return False, "Invalid latency: must be non-negative number"
        if not isinstance(runtime_data['health'], (int, float)) or not (0 <= runtime_data['health'] <= 1):
            return False, "Invalid health: must be float between 0 and 1"
        if not isinstance(runtime_data['failures'], int) or runtime_data['failures'] < 0:
            return False, "Invalid failures: must be non-negative integer"
        if not isinstance(runtime_data['services'], list) or len(runtime_data['services']) == 0:
            return False, "Invalid services: must be non-empty list"
        
        return True, None
    
    def get_noop_fallback(self):
        # Return a NOOP (no operation) runtime state for fallback
        return {
            'latency': 0,
            'health': 1.0,
            'failures': 0,
            'services': ['noop']
        }