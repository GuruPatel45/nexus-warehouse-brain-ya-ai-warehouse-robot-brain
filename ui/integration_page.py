import streamlit as st
import io
import sys
from modules.integration.shift_log_generator import generate_shift_log
from modules.integration.control_loop import run

st.title("🔄 Integrated Simulation")
st.write("Run the full warehouse control loop, synthesizing data across all 5 intelligence modules.")

col1, col2 = st.columns(2)
with col1:
    n_events = st.number_input("Number of Synthetic Events", min_value=1, max_value=200, value=75)
with col2:
    seed = st.number_input("Random Seed", value=42)

if st.button("Run Simulated Shift", type="primary"):
    with st.spinner("Generating shift log and running control loop..."):
        # 1. Generate events
        events = generate_shift_log(n_events=n_events, seed=seed)
        st.success(f"Generated {len(events)} events.")
        
        # 2. Capture stdout to display in UI
        old_stdout = sys.stdout
        sys.stdout = my_stdout = io.StringIO()
        
        try:
            # 3. Run control loop
            run(events)
        finally:
            sys.stdout = old_stdout
            
        output_text = my_stdout.getvalue()
        
        # Display the log
        st.subheader("Shift Log Execution Trace")
        with st.expander("View Full Console Trace", expanded=True):
            st.text(output_text)
        
        # Extract and display key metrics
        st.subheader("Simulation Metrics")
        colA, colB, colC = st.columns(3)
        colA.metric("Total Events Processed", len(events))
        
        damage_count = output_text.count("Triggering Module E")
        colB.metric("Expert Interventions", damage_count)
        
        dock_count = output_text.count("Module C simulating dock game")
        colC.metric("Dock Contentions Resolved", dock_count)
