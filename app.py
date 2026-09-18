import streamlit as st

st.set_page_config(
    page_title="AI Warehouse Brain",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the "premium" dark aesthetic
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Highlight titles */
    h1, h2, h3 {
        color: #00D2FF;
    }
</style>
""", unsafe_allow_html=True)

# Define pages
pages = {
    "Overview": [
        st.Page("ui/overview.py", title="Dashboard", icon="📊"),
    ],
    "Modules": [
        st.Page("ui/planning_page.py", title="Planning (Module A)", icon="🏗️"),
        st.Page("ui/uncertainty_page.py", title="Uncertainty (Module B)", icon="🎲"),
        st.Page("ui/game_page.py", title="Dock Game (Module C)", icon="🎮"),
        st.Page("ui/connectionist_page.py", title="Connectionist (Module D)", icon="🧠"),
        st.Page("ui/expert_system_page.py", title="Maintenance Expert (Module E)", icon="🛠️"),
    ],
    "Simulation": [
        st.Page("ui/integration_page.py", title="Integrated Simulation", icon="🔄"),
    ]
}

# Run navigation
pg = st.navigation(pages)
pg.run()
