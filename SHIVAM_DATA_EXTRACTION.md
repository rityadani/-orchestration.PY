# Shivam Runtime Data Extraction Guide

## 🎯 What Data You Need to Extract from Shivam

### 1. Runtime Metrics API
You need to call Shivam's runtime metrics API to get current system state:

```python
# Shivam API endpoint you need to call:
shivam_runtime_data = shivam_api.get_runtime_metrics()

# This should return:
{
    "latency": float,        # Current average response time in milliseconds
    "health": float,         # Overall system health score (0.0 to 1.0)
    "failures": int,         # Number of failed requests in last 5 minutes
    "services": list         # List of currently active services
}
```

### 2. Service Health Status
For each service in the `services` list, get detailed health:

```python
# For each service, call:
service_health = shivam_api.get_service_health(service_name)

# Use this to calculate overall health score
# health = average of all service health scores
```

### 3. Performance Metrics
Extract latency from Shivam's performance monitoring:

```python
# Shivam performance API:
latency_metrics = shivam_api.get_performance_metrics()
# Extract: average response time, p95 latency, etc.
```

### 4. Error/Failure Tracking
Get failure counts from Shivam's error monitoring:

```python
# Shivam error API:
error_counts = shivam_api.get_error_counts(time_window="5m")
# failures = total error count in time window
```

### 5. Service Discovery
Get the list of active services:

```python
# Shivam service registry:
active_services = shivam_api.get_active_services()
# services = list of service names currently running
```

## 🔌 Shivam API Methods You Need

Based on your RL Orchestrator requirements, call these Shivam APIs:

### Real-time Data Collection
```python
def collect_shivam_runtime_data():
    """Extract all required data from Shivam APIs"""
    try:
        # 1. Get performance metrics
        perf_data = shivam_api.get_runtime_metrics()

        # 2. Calculate health score
        services = shivam_api.get_active_services()
        health_scores = []
        for service in services:
            health = shivam_api.get_service_health(service)
            health_scores.append(health)

        # 3. Get failure counts
        failures = shivam_api.get_error_counts(minutes=5)

        # 4. Format for RL Orchestrator
        runtime_data = {
            "latency": perf_data.get("average_latency", 0),
            "health": sum(health_scores) / len(health_scores) if health_scores else 0,
            "failures": failures.get("total_errors", 0),
            "services": services
        }

        return runtime_data

    except Exception as e:
        # Fallback to safe defaults if Shivam APIs fail
        return {
            "latency": 100,  # Safe default
            "health": 0.8,   # Assume healthy
            "failures": 0,   # No failures
            "services": ["web", "db"]  # Known services
        }
```

### Decision Execution Feedback
After your RL Orchestrator returns a decision, you need to:

```python
def execute_decision_and_get_feedback(decision, original_runtime_data):
    """Execute decision through Shivam and collect outcome"""

    # 1. Send decision to Shivam (LOG ONLY - don't actually execute)
    # shivam_api.execute_decision(decision)  # DON'T CALL THIS YET

    # 2. For now, simulate what would happen and get feedback
    # In real integration, Shivam would execute and report back

    # 3. After execution, collect new runtime state
    new_runtime_data = collect_shivam_runtime_data()

    # 4. Determine success/failure based on outcome
    success = new_runtime_data["health"] > original_runtime_data["health"]
    failure = new_runtime_data["health"] < original_runtime_data["health"] * 0.8

    outcome = {
        "success": success,
        "failure": failure,
        "next_state": new_runtime_data
    }

    return outcome
```

## 📋 Shivam API Endpoints Checklist

**Required Shivam APIs for Integration:**

- [ ] `shivam_api.get_runtime_metrics()` → latency data
- [ ] `shivam_api.get_service_health(service_name)` → individual service health
- [ ] `shivam_api.get_active_services()` → list of running services
- [ ] `shivam_api.get_error_counts(time_window)` → failure counts
- [ ] `shivam_api.execute_decision(decision)` → execute orchestration actions (future)

## 🔄 Integration Flow

```
Shivam Runtime Events → Extract Data → RL Orchestrator → Decision → Execute via Shivam → Feedback → Learn
```

## ⚠️ Important: Start with Logging Only

**Phase 1 (Current)**: Extract data, make decisions, LOG what would happen
**Phase 2 (Future)**: Actually execute decisions through Shivam APIs

## 🧪 Testing Data Extraction

Create a test script to verify Shivam data extraction:

```python
# test_shivam_data.py
from your_shivam_client import ShivamAPI

shivam = ShivamAPI()
data = collect_shivam_runtime_data()
print("Shivam Runtime Data:", data)

# Verify format matches RL Orchestrator expectations
assert "latency" in data
assert "health" in data
assert "failures" in data
assert "services" in data
```

## 📊 Data Validation

Ensure Shivam data meets these criteria:
- `latency`: > 0, reasonable range (0-10000ms)
- `health`: 0.0 to 1.0
- `failures`: >= 0
- `services`: non-empty list of strings

This is what you need to extract from Shivam - the actual API calls and data formats!