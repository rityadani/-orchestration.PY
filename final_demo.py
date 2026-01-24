from rl_orchestrator_bridge import RLOOrchestratorBridge
import time
import json

def simulate_runtime_event(bridge, event_data, outcome):
    print(f"Processing event: {event_data}")
    decision = bridge.process_runtime_event(event_data)
    print(f"Decision: {decision}")
    
    # Simulate outcome
    time.sleep(0.1)  # Simulate time
    bridge.record_outcome(event_data, decision.get('rl_action', 0), outcome)
    print(f"Outcome recorded: {outcome}")
    
    # Verified artifacts: Log detailed trace
    with open('demo_artifacts.json', 'a') as f:
        json.dump({
            'event': event_data,
            'decision': decision,
            'outcome': outcome,
            'timestamp': time.time()
        }, f, indent=4)
        f.write('\n')

def main():
    bridge = RLOOrchestratorBridge()
    
    # Clear previous artifacts
    with open('demo_artifacts.json', 'w') as f:
        f.write('')
    
    # Simulate degraded service in prod
    event1 = {
        'latency': 600,
        'health': 0.5,
        'failures': 2,
        'services': ['web', 'db'],
        'environment': 'prod'
    }
    outcome1 = {
        'success': True, 
        'next_state': {'latency': 200, 'health': 0.9, 'failures': 0, 'services': ['web', 'db'], 'environment': 'prod'},
        'prev_health': 0.5
    }
    simulate_runtime_event(bridge, event1, outcome1)
    
    # Simulate failing service in dev
    event2 = {
        'latency': 1000,
        'health': 0.2,
        'failures': 5,
        'services': ['web'],
        'environment': 'dev'
    }
    outcome2 = {
        'failure': True, 
        'next_state': {'latency': 1000, 'health': 0.1, 'failures': 6, 'services': ['web'], 'environment': 'dev'},
        'prev_health': 0.2
    }
    simulate_runtime_event(bridge, event2, outcome2)
    
    # Simulate prod safety
    event3 = {
        'latency': 50,
        'health': 0.95,
        'failures': 0,
        'services': ['web', 'db', 'cache'],
        'environment': 'prod'
    }
    outcome3 = {
        'success': True, 
        'next_state': event3,
        'prev_health': 0.95
    }
    simulate_runtime_event(bridge, event3, outcome3)
    
    print("Demo completed. Check decision_traces.log, fusion_rl_summary.json, and demo_artifacts.json for verified artifacts.")

if __name__ == "__main__":
    main()