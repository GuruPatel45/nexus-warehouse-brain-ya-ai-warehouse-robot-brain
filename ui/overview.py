import streamlit as st

st.title("📊 Warehouse Brain Overview")
st.markdown("""
Welcome to the **Uncertainty-Aware Warehouse Robot Brain**. 

This system integrates five artificial intelligence modules to control an autonomous warehouse robot under uncertainty:

1. **Module A (Planning)**: Stack pallets using Goal Stack, POP, Hierarchical, and Reactive planning.
2. **Module B (Uncertainty)**: Evaluate sensor telemetry using Bayes, CF, DS, Fuzzy Logic, and BN.
3. **Module C (Game Playing)**: Resolve dock contentions using adversarial search (MiniMax, Alpha-Beta).
4. **Module D (Connectionist)**: Pattern recall (Hopfield) and temporal anomaly detection (RNN).
5. **Module E (Expert System)**: Diagnose faults using a forward-chaining rule engine.

Use the navigation menu to explore each module interactively, or go to the **Integrated Simulation** page to run the full warehouse control loop.
""")

st.info("👈 Please select a module from the sidebar to begin.")
