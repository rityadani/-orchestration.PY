class RuntimeStateAdapter:
    def adapt(self, runtime_data):
        # Convert runtime_data to RL state dict
        rl_state = {
            'latency_level': self._categorize_latency(runtime_data.get('latency', 0)),
            'health_level': runtime_data.get('health', 0),
            'failure_count': runtime_data.get('failures', 0),
            'service_count': len(runtime_data.get('services', []))
        }
        return rl_state

    def _categorize_latency(self, latency):
        if latency < 100:
            return 0
        elif latency < 500:
            return 1
        else:
            return 2