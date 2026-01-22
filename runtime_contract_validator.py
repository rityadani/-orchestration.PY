class RuntimeContractValidator:
    def validate(self, runtime_data):
        # Check if runtime_data has required fields
        required_fields = ['latency', 'health', 'failures', 'services']
        for field in required_fields:
            if field not in runtime_data:
                return False
        return True