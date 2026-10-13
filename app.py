import streamlit as st
import os
from ui.theme import inject_theme

st.set_page_config(
    page_title="NEXUS ROBOTICS // Warehouse Brain OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply master cyber theme styling
inject_theme()

# Sidebar Custom Branding
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.jpg")
    if os.path.exists(logo_path):
        st.image(logo_path, width=90)
    
    st.markdown("""
    <div style="margin-bottom: 1.2rem;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <h2 style="margin: 0; font-size: 1.5rem; font-weight: 800; letter-spacing: -0.02em;
                       background: linear-gradient(135deg, #00f2fe 0%, #7928ca 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                NEXUS-AGV
            </h2>
            <span class="cyber-badge badge-cyan" style="font-size: 0.65rem; padding: 2px 8px;">OS v3.0</span>
        </div>
        <p style="margin: 2px 0 0 0; color: #64748b; font-size: 0.8rem; font-family: 'Space Grotesk', sans-serif;">
            Autonomous Robotic Intelligence Engine
        </p>
    </div>
    
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(0, 242, 254, 0.15); border-radius: 12px; padding: 0.85rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 0.75rem; color: #94a3b8; font-weight: 600;">TELEMETRY LINK</span>
            <span style="display: flex; align-items: center; gap: 5px; font-size: 0.75rem; color: #00f5a0; font-weight: 700;">
                <span class="pulse-dot"></span> 100 Hz ACTIVE
            </span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 0.72rem; color: #cbd5e1;">
            <div>AGV Units: <b style="color: #00f2fe;">12 Sync</b></div>
            <div>Latency: <b style="color: #00f5a0;">1.4 ms</b></div>
            <div>Safety: <b style="color: #b388ff;">SIL-3 Max</b></div>
            <div>State: <b style="color: #f59e0b;">Nominal</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Define pages structure
pages = {
    "Mission Control": [
        st.Page("ui/overview.py", title="Command Dashboard", icon="🛰️"),
    ],
    "Cognitive Modules": [
        st.Page("ui/planning_page.py", title="Planning & Stacking (Mod A)", icon="🏗️"),
        st.Page("ui/uncertainty_page.py", title="Sensor Uncertainty (Mod B)", icon="🎲"),
        st.Page("ui/game_page.py", title="Adversarial Dock (Mod C)", icon="⚔️"),
        st.Page("ui/connectionist_page.py", title="Neural Associative (Mod D)", icon="🧠"),
        st.Page("ui/expert_system_page.py", title="Diagnostic Expert (Mod E)", icon="🛠️"),
    ],
    "Digital Twin": [
        st.Page("ui/integration_page.py", title="Control Loop Simulator", icon="⚡"),
    ]
}

# Run navigation
pg = st.navigation(pages)
pg.run()
