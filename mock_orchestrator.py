from rl_orchestrator_bridge import RLOOrchestratorBridge
import time
import logging
import numpy as np

logging.basicConfig(filename='orchestrator.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class MockOrchestrator:
    def __init__(self):
        self.bridge = RLOOrchestratorBridge()
        self.runtime_state = {
            'latency': 100,
            'health': 0.9,
            'failures': 0,
            'services': ['web', 'db'],
            'environment': 'prod'  # Add environment for safety
        }
    
    def simulate_runtime_event(self):
        # Simulate real runtime event (e.g., from Shivam)
        # In real implementation, this would poll or receive events
        self.runtime_state['latency'] += np.random.randint(-50, 50)  # Simulate fluctuation
        self.runtime_state['health'] = max(0, min(1, self.runtime_state['health'] + np.random.uniform(-0.1, 0.1)))
        self.runtime_state['failures'] = max(0, self.runtime_state['failures'] + np.random.randint(0, 2))
        
        logging.info(f"Simulated runtime event: {self.runtime_state}")
        return self.runtime_state
    
    def process_and_act(self):
        runtime_data = self.simulate_runtime_event()
        decision = self.bridge.process_runtime_event(runtime_data)
        
        # Simulate acting on decision (in real orchestrator, apply to services)
        self.apply_decision(decision)
        
        # Simulate outcome
        outcome = self.simulate_outcome(decision)
        self.bridge.record_outcome(runtime_data, decision.get('rl_action', 0), outcome)
        
        logging.info(f"Decision applied: {decision}, Outcome: {outcome}")
    
    def apply_decision(self, decision):
        action = decision.get('action')
        if action == 'scale_up':
            self.runtime_state['services'].append('new_service')
        elif action == 'scale_down':
            if len(self.runtime_state['services']) > 1:
                self.runtime_state['services'].pop()
        elif action == 'restart':
            self.runtime_state['health'] = min(1.0, self.runtime_state['health'] + 0.1)
        elif action == 'heal':
            self.runtime_state['failures'] = max(0, self.runtime_state['failures'] - 1)
        # monitor does nothing
    
    def simulate_outcome(self, decision):
        # Simulate success/failure based on decision and state
        success_prob = self.runtime_state['health'] * 0.8 + 0.2  # Higher health = higher success
        success = np.random.rand() < success_prob
        
        # Update state based on outcome
        if success:
            self.runtime_state['health'] = min(1.0, self.runtime_state['health'] + 0.05)
            self.runtime_state['latency'] = max(0, self.runtime_state['latency'] - 20)
        else:
            self.runtime_state['health'] = max(0, self.runtime_state['health'] - 0.1)
            self.runtime_state['latency'] += 50
        
        return {
            'success': success,
            'failure': not success,
            'next_state': self.runtime_state.copy(),
            'prev_health': decision.get('runtime_context', {}).get('health', 0.5)
        }

if __name__ == "__main__":
    orchestrator = MockOrchestrator()
    for _ in range(10):  # Simulate 10 cycles
        orchestrator.process_and_act()
        time.sleep(0.5)
    print("Mock orchestrator run completed. Check orchestrator.log and fusion_rl_summary.json")