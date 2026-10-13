import streamlit as st
import os
from ui.theme import render_page_header, render_cyber_card, render_html

# Top Header
render_page_header(
    title="NEXUS COMMAND // ROBOTIC INTELLIGENCE OS",
    subtitle="Centralized telemetry, multi-formalism reasoning, and real-time autonomous AGV fleet orchestration.",
    badge="GRID ONLINE",
    icon="🛰️"
)

# Hero Banner
banner_path = os.path.join(os.path.dirname(__file__), "..", "assets", "banner.jpg")
if os.path.exists(banner_path):
    render_html(
        '<div style="border-radius: 16px; overflow: hidden; border: 1px solid rgba(0, 242, 254, 0.25); '
        'box-shadow: 0 12px 35px rgba(0,0,0,0.6); margin-bottom: 2rem;">'
    )
    st.image(banner_path)
    render_html('</div>')

# Executive Live Metrics Row
st.markdown("### 📡 Real-Time Fleet & System Telemetry")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Fleet Operational Health", value="99.82%", delta="+0.4% efficiency")
with col2:
    st.metric(label="Active Cargo Pallets", value="1,842", delta="12 units in transit")
with col3:
    st.metric(label="Dock Conflict Rate", value="2.8%", delta="-1.1% arbitrated")
with col4:
    st.metric(label="Inference Latency", value="3.6 ms", delta="Sub-cycle real-time")

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Architecture Modules Cards
st.markdown("### 🧠 Autonomous Intelligence Modules")

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    content_a = (
        "<p style='color: #94a3b8; font-size: 0.95rem; line-height: 1.5; margin: 0 0 10px 0;'>"
        "Orchestrates robotic pallet manipulation through hybrid hierarchical and reactive planning. "
        "Automatically resolves physical disturbances and re-stacks misplaced warehouse blocks."
        "</p>"
        "<div style='display: flex; gap: 8px; flex-wrap: wrap;'>"
        "<span class='cyber-badge badge-cyan'>Goal Stack Planner</span>"
        "<span class='cyber-badge badge-purple'>Nonlinear (POP)</span>"
        "<span class='cyber-badge badge-emerald'>Hierarchical HTN</span>"
        "<span class='cyber-badge badge-rose'>Reactive Recovery</span>"
        "</div>"
    )
    render_cyber_card("🏗️ Module A: Task & Motion Planning", content_a, badge="OPTIMAL", color="cyan")

with row1_col2:
    content_b = (
        "<p style='color: #94a3b8; font-size: 0.95rem; line-height: 1.5; margin: 0 0 10px 0;'>"
        "Fuses noisy multimodal telemetry (optical crack severity, strain gauges, tilt sensors) "
        "using 6 complementary uncertainty theories to identify package and payload damage."
        "</p>"
        "<div style='display: flex; gap: 8px; flex-wrap: wrap;'>"
        "<span class='cyber-badge badge-cyan'>Bayesian Posterior</span>"
        "<span class='cyber-badge badge-purple'>Dempster-Shafer</span>"
        "<span class='cyber-badge badge-emerald'>Fuzzy Logic Control</span>"
        "<span class='cyber-badge badge-cyan'>Bayesian Networks</span>"
        "</div>"
    )
    render_cyber_card("🎲 Module B: Multimodal Uncertainty Fusion", content_b, badge="ACTIVE", color="emerald")

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    content_c = (
        "<p style='color: #94a3b8; font-size: 0.95rem; line-height: 1.5; margin: 0 0 10px 0;'>"
        "Resolves charging dock contention between competing AGVs using game-theoretic adversarial search, "
        "featuring MiniMax with alpha-beta pruning and iterative deepening."
        "</p>"
        "<div style='display: flex; gap: 8px; flex-wrap: wrap;'>"
        "<span class='cyber-badge badge-purple'>MiniMax Search</span>"
        "<span class='cyber-badge badge-cyan'>Alpha-Beta Pruning</span>"
        "<span class='cyber-badge badge-emerald'>Iterative Deepening</span>"
        "<span class='cyber-badge badge-rose'>Zero-Sum Matrix</span>"
        "</div>"
    )
    render_cyber_card("⚔️ Module C: Adversarial Dock Contention", content_c, badge="STANDBY", color="purple")

with row2_col2:
    content_d = (
        "<p style='color: #94a3b8; font-size: 0.95rem; line-height: 1.5; margin: 0 0 10px 0;'>"
        "Recovers corrupted sensor patterns via Hopfield associative attractor memory and forecasts "
        "temporal anomalies using recurrent neural networks (RNN)."
        "</p>"
        "<div style='display: flex; gap: 8px; flex-wrap: wrap;'>"
        "<span class='cyber-badge badge-cyan'>Hopfield Network</span>"
        "<span class='cyber-badge badge-purple'>Energy Landscapes</span>"
        "<span class='cyber-badge badge-emerald'>PyTorch RNN</span>"
        "<span class='cyber-badge badge-rose'>Time-Series Anomaly</span>"
        "</div>"
    )
    render_cyber_card("🧠 Module D: Connectionist & Temporal AI", content_d, badge="READY", color="cyan")

# Module E
content_e = (
    "<p style='color: #94a3b8; font-size: 0.95rem; line-height: 1.5; margin: 0 0 10px 0;'>"
    "Forward-chaining rule-based diagnostic engine executing maintenance triage on degraded AGV hardware, "
    "equipped with an interactive Knowledge Acquisition protocol for real-time rule injection."
    "</p>"
    "<div style='display: flex; gap: 8px; flex-wrap: wrap;'>"
    "<span class='cyber-badge badge-emerald'>Forward-Chaining Inferencing</span>"
    "<span class='cyber-badge badge-purple'>Symptom Conflict Resolution</span>"
    "<span class='cyber-badge badge-cyan'>Knowledge Base Editor</span>"
    "<span class='cyber-badge badge-rose'>Hardware Health Triage</span>"
    "</div>"
)
render_cyber_card("🛠️ Module E: Maintenance Diagnostic Expert", content_e, badge="ONLINE", color="emerald")

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

# Warehouse Sector Grid Visualizer
st.markdown("### 🏭 Physical Facility Sectors")
sector_cols = st.columns(4)
sectors = [
    ("Sector Alpha", "Inbound Pallet Induction", "🟢 100% Operational", "#00f5a0"),
    ("Sector Beta", "High-Bay Vertical Stacking", "🟢 Stacking in Progress", "#00f2fe"),
    ("Sector Gamma", "Automated Fast-Charge Docks", "🟡 2 Units Queued", "#f59e0b"),
    ("Sector Delta", "Outbound Dispatch & Sorting", "🟢 Nominal Throughput", "#00f5a0")
]

for col, (name, role, status, color) in zip(sector_cols, sectors):
    with col:
        sector_html = (
            f'<div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); '
            f'border-radius: 12px; padding: 1.1rem; border-top: 3px solid {color};">'
            f'<div style="font-weight: 700; font-size: 1.05rem; color: #f8fafc; margin-bottom: 4px;">{name}</div>'
            f'<div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 8px;">{role}</div>'
            f'<div style="font-size: 0.85rem; font-weight: 600; color: {color};">{status}</div>'
            f'</div>'
        )
        render_html(sector_html)
