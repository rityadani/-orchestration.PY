import json
import os
import numpy as np
from collections import defaultdict

class RLDecisionLayer:
    def __init__(self, state_space_size=100, action_space_size=10, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.state_space_size = state_space_size
        self.action_space_size = action_space_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: np.zeros(action_space_size))
        self.summary_file = 'fusion_rl_summary.json'
        self.load_summary()

    def load_summary(self):
        if os.path.exists(self.summary_file):
            with open(self.summary_file, 'r') as f:
                data = json.load(f)
                self.q_table = defaultdict(lambda: np.zeros(self.action_space_size), data.get('q_table', {}))
                for k, v in self.q_table.items():
                    self.q_table[k] = np.array(v)

    def save_summary(self):
        data = {
            'q_table': {k: v.tolist() for k, v in self.q_table.items()},
            'last_updated': str(np.datetime64('now'))
        }
        with open(self.summary_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get_state_key(self, state):
        # Convert state dict to a hashable key
        return str(sorted(state.items()))

    def process_state(self, rl_state):
        state_key = self.get_state_key(rl_state)
        if np.random.rand() < self.epsilon:
            action = int(np.random.randint(self.action_space_size))
        else:
            action = int(np.argmax(self.q_table[state_key]))
        return action

    def record_action_result(self, rl_state, action, reward, next_rl_state):
        state_key = self.get_state_key(rl_state)
        next_state_key = self.get_state_key(next_rl_state)
        
        old_value = self.q_table[state_key][action]
        next_max = np.max(self.q_table[next_state_key])
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * next_max - old_value)
        self.q_table[state_key][action] = new_value
        
        self.save_summary()
        return new_value - old_value  # reward change

    def get_q_table_summary(self):
        return dict(self.q_table)