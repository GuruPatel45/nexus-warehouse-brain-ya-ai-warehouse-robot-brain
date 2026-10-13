import streamlit as st
import io
import sys
import pandas as pd
from ui.theme import render_page_header, render_cyber_card, render_html
from modules.integration.shift_log_generator import generate_shift_log
from modules.integration.control_loop import run

render_page_header(
    title="DIGITAL TWIN // LIVE CONTROL LOOP",
    subtitle="Full-scale autonomous warehouse shift simulation synthesizing all 5 cognitive modules into a unified cybernetic control loop.",
    badge="DIGITAL TWIN ONLINE",
    icon="⚡"
)

st.markdown("### 🎛️ Simulation Parameters & Mission Profile")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    scenario_profile = st.selectbox(
        "Warehouse Operating Condition",
        ["Standard Production Shift", "Heavy Pallet Load & High Turbulence", "Peak Congestion (Dock Starvation)"]
    )
with col2:
    if scenario_profile == "Standard Production Shift":
        default_events = 75
    elif scenario_profile == "Heavy Pallet Load & High Turbulence":
        default_events = 100
    else:
        default_events = 50
    n_events = st.number_input("Event Horizon (Telemetry Points)", min_value=10, max_value=250, value=default_events)
with col3:
    seed = st.number_input("RNG Determinism Seed", value=42)

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

if st.button("🚀 INITIALIZE AUTONOMOUS SHIFT SIMULATION", type="primary", use_container_width=True):
    with st.spinner("Synthesizing multi-agent dispatch queue and executing real-time control loop..."):
        # 1. Generate events
        events = generate_shift_log(n_events=n_events, seed=seed)
        
        # 2. Capture stdout to display in UI
        old_stdout = sys.stdout
        sys.stdout = my_stdout = io.StringIO()
        
        try:
            # 3. Run control loop
            run(events)
        finally:
            sys.stdout = old_stdout
            
        output_text = my_stdout.getvalue()
        
        # Extract metrics
        damage_count = output_text.count("Triggering Module E")
        dock_count = output_text.count("Module C simulating dock game")
        reactive_count = output_text.count("Reactive actions taken")
        
        # Display KPI HUD
        st.markdown("### 📊 Shift Performance Analytics & KPI HUD")
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric("Total Events Handled", f"{len(events)}", "100% throughput")
        with kpi2:
            st.metric("Expert Diagnoses (Mod E)", f"{damage_count}", "Payload defects")
        with kpi3:
            st.metric("Dock Contention Resolves (Mod C)", f"{dock_count}", "Adversarial arbitrations")
        with kpi4:
            st.metric("Reactive Replans (Mod A)", f"{reactive_count}", "Drop recovery")
            
        # Event Distribution
        event_types = {}
        for ev in events:
            t = ev.get("type", "unknown")
            event_types[t] = event_types.get(t, 0) + 1
            
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("#### 📡 Telemetry Stream Distribution")
        
        type_cols = st.columns(len(event_types))
        type_labels = {
            "sensor_reading": ("Sensor Telemetry", "#00f2fe"),
            "disturbance": ("Physical Disturbances", "#ff007a"),
            "dock_request": ("Dock Arbitration Requests", "#b388ff")
        }
        for col, (etype, count) in zip(type_cols, event_types.items()):
            label, color = type_labels.get(etype, (etype, "#00f5a0"))
            with col:
                render_html(f"""
                <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.06); 
                            border-top: 3px solid {color}; border-radius: 10px; padding: 0.9rem; text-align: center;">
                    <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">{label}</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: {color}; margin-top: 2px;">{count}</div>
                    <div style="font-size: 0.75rem; color: #64748b;">{(count/len(events))*100:.1f}% of total</div>
                </div>
                """)
                
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        # Cyber Terminal Log Trace
        st.markdown("#### 💻 Real-Time Supervisory Terminal Log")
        
        # Colorize terminal lines
        formatted_lines = []
        for line in output_text.splitlines():
            line_str = line
            if "Event" in line:
                line_str = f"<span style='color: #00f2fe; font-weight: bold;'>{line}</span>"
            elif "Triggering Module E" in line or "REACTIVE" in line:
                line_str = f"<span style='color: #ff007a; font-weight: bold;'>{line}</span>"
            elif "Module C simulating" in line:
                line_str = f"<span style='color: #b388ff;'>{line}</span>"
            elif "Damage suspected: False" in line:
                line_str = f"<span style='color: #00f5a0;'>{line}</span>"
            elif "Winner:" in line:
                line_str = f"<span style='color: #f59e0b; font-weight: bold;'>{line}</span>"
            else:
                line_str = f"<span style='color: #94a3b8;'>{line}</span>"
            formatted_lines.append(line_str)
            
        terminal_html = f"""
        <div style="background: #050811; border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; 
                    padding: 1.25rem; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; 
                    max-height: 480px; overflow-y: auto; line-height: 1.6; box-shadow: inset 0 0 20px rgba(0,0,0,0.8);">
            {'<br>'.join(formatted_lines)}
        </div>
        """
        render_html(terminal_html)
