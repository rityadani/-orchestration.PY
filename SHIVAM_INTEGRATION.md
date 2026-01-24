# Shivam Runtime Integration Interface

## 🔗 What You Need from Shivam

### 1. Runtime Data Input Format
Your RL Orchestrator expects runtime data in this exact format:

```python
runtime_data = {
    "latency": float,        # Current latency in ms (e.g., 150.5)
    "health": float,         # System health score 0.0-1.0 (e.g., 0.85)
    "failures": int,         # Number of recent failures (e.g., 3)
    "services": list         # List of active services (e.g., ["web", "db", "cache"])
}
```

### 2. Runtime Event Stream
You need Shivam to provide real-time runtime events through this interface:

```python
# Shivam should call this method whenever runtime state changes
rl_orchestrator.process_runtime_event(runtime_data)
```

### 3. Outcome Feedback Loop
After each decision, Shivam must provide feedback:

```python
# Shivam calls this after decision execution
rl_orchestrator.record_outcome(runtime_data, action_taken, outcome)
```

Where `outcome` is:
```python
outcome = {
    "success": bool,        # True if decision succeeded
    "failure": bool,        # True if decision failed
    "next_state": dict      # Updated runtime_data after decision
}
```

## 📤 What Shivam Gets from Your System

### 1. Decision Output Format
Your system returns decisions in this format:

```python
decision = {
    "action": str,          # Action to take: "scale_up", "scale_down", "restart", "heal", "monitor"
    "target": str,          # Target service: "service"
    "runtime_context": dict # Original runtime data for context
    "rl_action": int        # Internal RL action ID (0-4)
}
```

### 2. Safe Decision Guarantee
- All decisions are validated and safe
- Unsafe RL suggestions are automatically downgraded
- Never returns actions that could harm the system

### 3. Learning Integration
- RL learns from real outcomes
- Q-table updates automatically
- Performance improves over time

## 🔌 Integration Points

### Shivam → RL Orchestrator
```python
from rl_orchestrator_bridge import RLOOrchestratorBridge

# Initialize
orchestrator = RLOOrchestratorBridge()

# Shivam calls this on runtime events
decision = orchestrator.process_runtime_event(shivam_runtime_data)

# Shivam executes the decision (but NEVER executes infra directly)
# Just log what would happen

# Shivam provides feedback
orchestrator.record_outcome(shivam_runtime_data, decision['rl_action'], outcome)
```

### Key Integration Files
- `rl_orchestrator_bridge.py` - Main interface class
- `runtime_contract_validator.py` - Validates Shivam inputs
- `runtime_state_adapter.py` - Converts Shivam data to RL format

## ⚠️ Important Notes

1. **Never Execute Infrastructure**: The system only returns decisions, never executes them
2. **Real Runtime Data**: Use actual Shivam metrics, not simulated data
3. **Feedback Loop**: Always call `record_outcome` after decisions for learning
4. **Safety First**: The system will override unsafe RL decisions
5. **Logging**: All decisions are logged in `decision_traces.log`

## 🧪 Testing Integration

Use the existing `final_demo.py` as a reference for how to call the interfaces. Replace the simulated data with real Shivam runtime data.

## 📊 Monitoring

Launch the dashboard to monitor RL learning:
```bash
streamlit run dashboard.py
```

This will show you how RL is learning from Shivam data and making better decisions over time.