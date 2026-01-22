import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time

st.set_page_config(page_title="RL Orchestration Dashboard", page_icon="🤖", layout="wide")

st.title("🚀 RL Orchestration Dashboard")
st.markdown("**Real-time monitoring of your Reinforcement Learning orchestration system**")

# Auto-refresh
auto_refresh = st.sidebar.checkbox("Auto-refresh (every 5s)", value=True)
if auto_refresh:
    time.sleep(5)
    st.rerun()

# Sidebar controls
st.sidebar.header("🎛️ Controls")
num_traces = st.sidebar.slider("Number of recent traces to show", 5, 50, 10)
show_rewards = st.sidebar.checkbox("Show reward trends", value=True)
show_q_heatmap = st.sidebar.checkbox("Show Q-table heatmap", value=True)

# Load Q-table
@st.cache_data(ttl=10)
def load_q_table():
    try:
        with open('fusion_rl_summary.json', 'r') as f:
            data = json.load(f)
        q_table = data.get('q_table', {})
        last_updated = data.get('last_updated', 'Never')
        return q_table, last_updated
    except FileNotFoundError:
        return {}, 'Never'

# Load decision traces
@st.cache_data(ttl=10)
def load_traces():
    traces = []
    try:
        with open('decision_traces.log', 'r') as f:
            lines = f.readlines()
        
        i = 0
        while i < len(lines):
            line = lines[i]
            if '{' in line:
                parts = line.split(' - ', 1)
                if len(parts) > 1:
                    timestamp = parts[0]
                    json_part = parts[1].strip()
                    try:
                        trace = json.loads(json_part)
                        trace['timestamp'] = timestamp
                        
                        # Check next lines for reward
                        j = i + 1
                        while j < len(lines) and 'Reward recorded:' in lines[j]:
                            reward_line = lines[j]
                            if 'Reward recorded:' in reward_line:
                                reward_part = reward_line.split('Reward recorded: ')[1].split(',')[0].strip()
                                try:
                                    trace['reward'] = float(reward_part)
                                except:
                                    pass
                            j += 1
                        i = j - 1  # Skip the reward lines
                        
                        traces.append(trace)
                    except:
                        pass
            i += 1
    except FileNotFoundError:
        pass
    return traces

q_table, last_updated = load_q_table()
traces = load_traces()

# Main metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("States Learned", len(q_table))
with col2:
    st.metric("Total Decisions", len(traces))
with col3:
    success_rate = len([t for t in traces if t.get('reward') == 1]) / len(traces) * 100 if traces else 0
    st.metric("Success Rate", f"{success_rate:.1f}%")
with col4:
    st.metric("Last Updated", last_updated)

# RL Q-Table Section
st.header("🧠 RL Q-Table")
if q_table:
    df_q = pd.DataFrame.from_dict(q_table, orient='index')
    df_q.columns = [f'Action {i}' for i in range(len(df_q.columns))]

    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(df_q.style.highlight_max(axis=1, color='lightgreen'), height=300)

    with col2:
        if show_q_heatmap:
            fig, ax = plt.subplots(figsize=(6, 4))
            im = ax.imshow(df_q.values, cmap='viridis', aspect='auto')
            ax.set_xticks(range(len(df_q.columns)))
            ax.set_xticklabels(df_q.columns, rotation=45)
            ax.set_yticks(range(len(df_q.index)))
            ax.set_yticklabels([f'State {i}' for i in range(len(df_q.index))])
            ax.set_title("Q-Table Heatmap")
            plt.colorbar(im, ax=ax)
            st.pyplot(fig)

    # Best actions per state
    st.subheader("Best Actions per State")
    best_actions = df_q.idxmax(axis=1)
    st.write(best_actions)

else:
    st.info("No Q-table data yet. Run some decisions first!")

# Decision Traces Section
st.header("📋 Decision Traces")
if traces:
    df_traces = pd.DataFrame(traces[-num_traces:])

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        action_filter = st.multiselect("Filter by RL Action", options=sorted(set(df_traces['rl_action'].dropna())), default=[])
    with col2:
        safety_filter = st.multiselect("Filter by Safety Decision", options=sorted(set(df_traces['safety_decision'].dropna().apply(lambda x: x.get('action')))), default=[])

    if action_filter:
        df_traces = df_traces[df_traces['rl_action'].isin(action_filter)]
    if safety_filter:
        df_traces = df_traces[df_traces['safety_decision'].apply(lambda x: x.get('action') if isinstance(x, dict) else None).isin(safety_filter)]

    st.dataframe(df_traces, height=400)

    # Reward analysis
    if show_rewards:
        st.subheader("💰 Reward Analysis")
        rewards = df_traces['reward'].dropna()
        if not rewards.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                rewards.plot(ax=ax, marker='o')
                ax.set_title("Rewards Over Time")
                ax.set_xlabel("Decision #")
                ax.set_ylabel("Reward")
                st.pyplot(fig)

            with col2:
                reward_counts = rewards.value_counts()
                fig, ax = plt.subplots()
                reward_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%')
                ax.set_title("Reward Distribution")
                st.pyplot(fig)

else:
    st.info("No decision traces yet. Run the orchestrator!")

# Action Distribution
st.header("🎯 Action Distribution")
actions = [t.get('rl_action') for t in traces if 'rl_action' in t]
if actions:
    action_counts = pd.Series(actions).value_counts()
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        action_counts.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title("RL Actions Chosen")
        ax.set_xlabel("Action ID")
        ax.set_ylabel("Count")
        plt.xticks(rotation=0)
        st.pyplot(fig)

    with col2:
        safety_actions = [t.get('safety_decision', {}).get('action') for t in traces if isinstance(t.get('safety_decision'), dict)]
        if safety_actions:
            safety_counts = pd.Series(safety_actions).value_counts()
            fig, ax = plt.subplots()
            safety_counts.plot(kind='bar', ax=ax, color='lightcoral')
            ax.set_title("Safety-Modified Actions")
            ax.set_xlabel("Action")
            ax.set_ylabel("Count")
            plt.xticks(rotation=45)
            st.pyplot(fig)

# System Health
st.header("🏥 System Health Indicators")
if traces:
    recent_traces = traces[-20:]  # Last 20 decisions

    health_scores = [t.get('runtime_state', {}).get('health', 0) for t in recent_traces]
    latency_scores = [t.get('runtime_state', {}).get('latency', 0) for t in recent_traces]
    failure_counts = [t.get('runtime_state', {}).get('failures', 0) for t in recent_traces]

    col1, col2, col3 = st.columns(3)
    with col1:
        fig, ax = plt.subplots()
        ax.plot(health_scores, marker='o', color='green')
        ax.set_title("Recent Health Scores")
        ax.set_ylim(0, 1)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        ax.plot(latency_scores, marker='o', color='orange')
        ax.set_title("Recent Latency")
        st.pyplot(fig)

    with col3:
        fig, ax = plt.subplots()
        ax.plot(failure_counts, marker='o', color='red')
        ax.set_title("Recent Failures")
        st.pyplot(fig)

# Learning Progress
st.header("📈 Learning Progress")
if len(traces) > 1:
    cumulative_rewards = []
    total = 0
    for t in traces:
        reward = t.get('reward')
        if reward is not None:
            total += reward
            cumulative_rewards.append(total)

    if cumulative_rewards:
        fig, ax = plt.subplots()
        ax.plot(cumulative_rewards, marker='o')
        ax.set_title("Cumulative Rewards (Learning Progress)")
        ax.set_xlabel("Decisions")
        ax.set_ylabel("Total Reward")
        st.pyplot(fig)

st.markdown("---")
st.caption("Advanced RL Orchestration Monitoring Dashboard")