from rl_orchestrator_bridge import RLOOrchestratorBridge
import time

def simulate_runtime_event(bridge, event_data, outcome):
    print(f"Processing event: {event_data}")
    decision = bridge.process_runtime_event(event_data)
    print(f"Decision: {decision}")
    
    # Simulate outcome
    time.sleep(0.1)  # Simulate time
    bridge.record_outcome(event_data, decision.get('rl_action', 0), outcome)
    print(f"Outcome recorded: {outcome}")

def main():
    bridge = RLOOrchestratorBridge()
    
    # Simulate degraded service
    event1 = {
        'latency': 600,
        'health': 0.5,
        'failures': 2,
        'services': ['web', 'db']
    }
    outcome1 = {'success': True, 'next_state': {'latency': 200, 'health': 0.9, 'failures': 0, 'services': ['web', 'db']}}
    simulate_runtime_event(bridge, event1, outcome1)
    
    # Simulate failing service
    event2 = {
        'latency': 1000,
        'health': 0.2,
        'failures': 5,
        'services': ['web']
    }
    outcome2 = {'failure': True, 'next_state': {'latency': 1000, 'health': 0.1, 'failures': 6, 'services': ['web']}}
    simulate_runtime_event(bridge, event2, outcome2)
    
    # Simulate prod safety
    event3 = {
        'latency': 50,
        'health': 0.95,
        'failures': 0,
        'services': ['web', 'db', 'cache']
    }
    outcome3 = {'success': True, 'next_state': event3}
    simulate_runtime_event(bridge, event3, outcome3)
    
    print("Demo completed. Check decision_traces.log and fusion_rl_summary.json")

if __name__ == "__main__":
    main()