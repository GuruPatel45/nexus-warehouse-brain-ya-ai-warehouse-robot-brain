import streamlit as st
import pandas as pd
from modules.uncertainty.compare import TEST_CASES, evaluate_all_methods
from modules.uncertainty.nonmonotonic import sensor_reading_to_facts

st.title("🎲 Uncertainty (Module B)")
st.write("Determine if a box is damaged using 6 different uncertainty formalisms.")

tab1, tab2 = st.tabs(["Interactive Inference", "Unified Comparison Table"])

with tab1:
    st.subheader("Sensor Input")
    col1, col2, col3 = st.columns(3)
    with col1:
        weight_dev = st.slider("Weight Deviation (%)", 0, 100, 20)
    with col2:
        crack_sev = st.slider("Crack Severity (%)", 0, 100, 10)
    with col3:
        tilt = st.checkbox("Tilt Sensor Triggered", value=True)
        
    reading = {
        "weight_deviation_pct": weight_dev,
        "crack_severity_pct": crack_sev,
        "tilt_triggered": tilt
    }
    
    if st.button("Evaluate All Methods", type="primary"):
        st.write("**Extracted Facts:**")
        st.code(sensor_reading_to_facts(reading))
        
        results = evaluate_all_methods(reading)
        
        st.markdown("### Results")
        colA, colB, colC = st.columns(3)
        colA.metric("Nonmonotonic", results["nonmonotonic"])
        colB.metric("Bayes Posterior", f"{results['bayes']:.4f}")
        colC.metric("Certainty Factor", f"{results['cf']:.4f}")
        
        colD, colE, colF = st.columns(3)
        colD.metric("Bayesian Network", f"{results['bn']:.4f}")
        ds = results['ds']
        colE.metric("Dempster-Shafer (Bel, Pl)", f"({ds[0]:.3f}, {ds[1]:.3f})")
        colF.metric("Fuzzy Score", f"{results['fuzzy']:.2f}")
        
with tab2:
    st.subheader("Unified Comparison Table (10 Test Cases)")
    st.write("Identifies disagreements between the uncertainty reasoning methods.")
    
    rows = []
    for tc in TEST_CASES:
        res = evaluate_all_methods(tc)
        rows.append({
            "Case": tc["id"],
            "Weight Dev": tc["weight_deviation_pct"],
            "Crack Sev": tc["crack_severity_pct"],
            "Tilt": tc["tilt_triggered"],
            "Nonmonotonic": res["nonmonotonic"],
            "Bayes": round(res["bayes"], 4),
            "CF": round(res["cf"], 4),
            "BN": round(res["bn"], 4),
            "DS (Bel, Pl)": f"({res['ds'][0]:.2f}, {res['ds'][1]:.2f})",
            "Fuzzy": round(res["fuzzy"], 2)
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("""
    **Known Disagreements:**
    - **TC-B3 (w=70, c=5, t=False):** Nonmonotonic logic says NotDamaged because weight deviation doesn't trigger its rule, but continuous methods (Bayes, CF, Fuzzy) say Damaged because 70% weight deviation adds enough evidence.
    - **TC-B5 (w=20, c=10, t=True):** Nonmonotonic logic says Damaged because tilt is True, but Fuzzy logic says NotDamaged because it only looks at continuous variables (weight/crack) which are low.
    """)
