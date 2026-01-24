from rl_decision_layer import RLDecisionLayer
from runtime_contract_validator import RuntimeContractValidator
from runtime_state_adapter import RuntimeStateAdapter
from app_spec_validator import AppSpecValidator
from safety_guard import SafetyGuard
import json
import logging

logging.basicConfig(filename='decision_traces.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class RLOOrchestratorBridge:
    def __init__(self):
        self.rl_layer = RLDecisionLayer()
        self.contract_validator = RuntimeContractValidator()
        self.state_adapter = RuntimeStateAdapter()
        self.spec_validator = AppSpecValidator()
        self.safety_guard = SafetyGuard()

    def process_runtime_event(self, runtime_data):
        # Step 1: Validate runtime contract
        is_valid, error_msg = self.contract_validator.validate(runtime_data)
        if not is_valid:
            logging.warning(f"Runtime data invalid: {error_msg}. Using NOOP fallback.")
            runtime_data = self.contract_validator.get_noop_fallback()  # NOOP fallback

        # Step 2: Adapt to RL state
        rl_state = self.state_adapter.adapt(runtime_data)

        # Step 3: Get RL decision
        rl_action = self.rl_layer.process_state(rl_state)

        # Step 4: Wrap RL action into app_spec
        app_spec = self._create_app_spec_from_action(rl_action, runtime_data)

        # Step 5: Validate spec
        spec_valid = self.spec_validator.validate(app_spec)
        if not spec_valid:
            app_spec = self._downgrade_spec(app_spec)

        # Step 6: Safety guard
        final_decision = self.safety_guard.guard(app_spec)
        final_decision['rl_action'] = rl_action  # For recording

        # Log the decision trace
        trace = {
            'runtime_state': runtime_data,
            'rl_state': rl_state,
            'rl_action': rl_action,
            'app_spec': app_spec,
            'spec_valid': spec_valid,
            'safety_decision': final_decision,
            'reward': None  # To be set later
        }
        logging.info(json.dumps(trace))

        return final_decision

    def _create_app_spec_from_action(self, action, runtime_data):
        # Map action index to spec
        action_map = {
            0: {'action': 'scale_up', 'target': 'service'},
            1: {'action': 'scale_down', 'target': 'service'},
            2: {'action': 'restart', 'target': 'service'},
            3: {'action': 'heal', 'target': 'service'},
            4: {'action': 'monitor', 'target': 'service'},
            # Add more as needed
        }
        spec = action_map.get(action, {'action': 'monitor', 'target': 'service'})
        spec['runtime_context'] = runtime_data
        return spec

    def _downgrade_spec(self, spec):
        # Downgrade unsafe spec to safe one
        spec['action'] = 'monitor'
        return spec

    def record_outcome(self, runtime_data, action, outcome):
        rl_state = self.state_adapter.adapt(runtime_data)
        next_runtime_data = outcome.get('next_state', runtime_data)
        next_rl_state = self.state_adapter.adapt(next_runtime_data)
        reward = self._calculate_reward(outcome)
        reward_change = self.rl_layer.record_action_result(rl_state, action, reward, next_rl_state)
        
        # Update last log with reward
        # Note: In real implementation, might need to store traces and update
        logging.info(f"Reward recorded: {reward}, Change: {reward_change}")

    def _calculate_reward(self, outcome):
        # Extended reward function based on runtime metrics
        reward = 0
        next_state = outcome.get('next_state', {})
        
        # Base reward for success/failure
        if outcome.get('success'):
            reward += 1
        elif outcome.get('failure'):
            reward -= 1
        
        # Bonus/penalty based on health improvement
        health_improvement = next_state.get('health', 0) - outcome.get('prev_health', 0)
        reward += health_improvement * 0.5  # Scale health changes
        
        # Penalty for high latency
        latency = next_state.get('latency', 0)
        if latency > 500:
            reward -= 0.5
        elif latency < 100:
            reward += 0.2
        
        # Penalty for failures
        failures = next_state.get('failures', 0)
        reward -= failures * 0.1
        
        return reward