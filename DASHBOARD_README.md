# Advanced RL Orchestration Dashboard

## 🚀 Features

### Real-time Monitoring
- **Auto-refresh**: Updates every 5 seconds
- **Live metrics**: States learned, decisions made, success rate
- **Last updated timestamp**

### 🧠 RL Insights
- **Q-Table visualization**: Full table with highlighting
- **Heatmap**: Visual Q-value distribution
- **Best actions**: Optimal actions per state

### 📋 Decision Analysis
- **Trace filtering**: Filter by RL action or safety decision
- **Reward trends**: Time series and distribution charts
- **Detailed traces**: Full decision context

### 🎯 Action Analytics
- **RL action distribution**: What actions RL chooses
- **Safety modifications**: How safety guard changes decisions

### 🏥 System Health
- **Health scores**: Recent system health trends
- **Latency monitoring**: Performance over time
- **Failure tracking**: Error patterns

### 📈 Learning Progress
- **Cumulative rewards**: Overall learning trajectory
- **Success metrics**: Performance indicators

## 🎛️ Controls
- **Sidebar toggles**: Enable/disable features
- **Sliders**: Adjust trace display count
- **Filters**: Interactive data exploration

## 🏃‍♂️ Running the Dashboard
```bash
streamlit run dashboard.py
```

Open http://localhost:8503 in your browser.

## 📊 Data Sources
- `fusion_rl_summary.json`: Q-table and learning data
- `decision_traces.log`: Decision history and outcomes

Built for real-time RL orchestration monitoring! 🤖