import streamlit as st
import pandas as pd
from ui.theme import render_page_header, render_cyber_card
from modules.uncertainty.compare import TEST_CASES, evaluate_all_methods
from modules.uncertainty.nonmonotonic import sensor_reading_to_facts

render_page_header(
    title="MULTIMODAL UNCERTAINTY FUSION MATRIX",
    subtitle="Arbitrating noisy sensor telemetry across 6 complementary uncertainty theories to assess payload damage.",
    badge="MODULE B",
    icon="🎲"
)

tab1, tab2 = st.tabs(["🎛️ Live Sensor Diagnostic Studio", "📊 Multi-Method Disagreement Matrix (10 Cases)"])

with tab1:
    st.markdown("### 📡 Real-Time Telemetry Inputs")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem;">
            <div style="font-weight: 700; color: #00f2fe; font-size: 0.85rem; letter-spacing: 0.05em;">⚖️ STRAIN GAUGE</div>
            <div style="color: #94a3b8; font-size: 0.75rem;">Package Weight Deviation</div>
        </div>
        """, unsafe_allow_html=True)
        weight_dev = st.slider("Deviation Pct (%)", 0, 100, 25, label_visibility="collapsed")
        
    with col2:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(121, 40, 202, 0.2); border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem;">
            <div style="font-weight: 700; color: #b388ff; font-size: 0.85rem; letter-spacing: 0.05em;">👁️ OPTICAL CAMERA</div>
            <div style="color: #94a3b8; font-size: 0.75rem;">Surface Crack Severity</div>
        </div>
        """, unsafe_allow_html=True)
        crack_sev = st.slider("Crack Severity Pct (%)", 0, 100, 15, label_visibility="collapsed")
        
    with col3:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(0, 245, 160, 0.2); border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem;">
            <div style="font-weight: 700; color: #00f5a0; font-size: 0.85rem; letter-spacing: 0.05em;">📐 INERTIAL GYROSCOPE</div>
            <div style="color: #94a3b8; font-size: 0.75rem;">Tri-Axis Tilt Sensor Trigger</div>
        </div>
        """, unsafe_allow_html=True)
        tilt = st.checkbox("Tilt Threshold Exceeded (>15°)", value=True)
        
    reading = {
        "weight_deviation_pct": weight_dev,
        "crack_severity_pct": crack_sev,
        "tilt_triggered": tilt
    }
    
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    
    if st.button("⚡ EXECUTE MULTI-FORMALISM ARBITRATION", type="primary", use_container_width=True):
        facts = sensor_reading_to_facts(reading)
        results = evaluate_all_methods(reading)
        
        # Calculate consensus
        is_damaged_bayes = results['bayes'] > 0.5
        is_damaged_nonmono = results['nonmonotonic'] == 'Damaged'
        is_damaged_fuzzy = results['fuzzy'] > 50.0
        
        score_avg = (results['bayes'] + (results['cf'] + 1)/2 + results['bn'] + results['fuzzy']/100) / 4.0
        
        if score_avg > 0.55 or is_damaged_nonmono:
            banner_color = "#ff007a"
            verdict_text = "⚠️ PAYLOAD ANOMALY CONFIRMED: REJECT & DISPATCH TO MAINTENANCE"
            verdict_badge = "REJECT / QUARANTINE"
        else:
            banner_color = "#00f5a0"
            verdict_text = "✅ PAYLOAD NOMINAL: CLEARED FOR AUTOMATED VERTICAL STACKING"
            verdict_badge = "CLEARED / OPTIMAL"
            
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.85); border: 2px solid {banner_color}; border-radius: 14px; 
                    padding: 1.25rem 1.75rem; margin: 1.5rem 0; box-shadow: 0 0 25px {banner_color}33;
                    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;">
                    FUSION CONSENSUS VERDICT
                </div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin-top: 4px;">
                    {verdict_text}
                </div>
            </div>
            <div class="cyber-badge" style="background: {banner_color}22; border: 1px solid {banner_color}; color: {banner_color}; font-size: 0.85rem; padding: 6px 16px;">
                {verdict_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Formalisms Grid
        st.markdown("#### 🔬 Formalism Probability & Metric Matrix")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("1. Bayesian Posterior", f"{results['bayes']*100:.1f}%", f"{results['bayes']:.4f} P(D|E)")
        with m_col2:
            st.metric("2. Certainty Factor (CF)", f"{results['cf']:+.3f}", "Range [-1.0, +1.0]")
        with m_col3:
            st.metric("3. Bayesian Network (DAG)", f"{results['bn']*100:.1f}%", f"{results['bn']:.4f} Exact VE")
            
        m_col4, m_col5, m_col6 = st.columns(3)
        with m_col4:
            ds = results['ds']
            st.metric("4. Dempster-Shafer Interval", f"[{ds[0]:.2f}, {ds[1]:.2f}]", "Belief ➔ Plausibility")
        with m_col5:
            st.metric("5. Fuzzy Logic Score", f"{results['fuzzy']:.1f} / 100", "Centroid Defuzzified")
        with m_col6:
            nonmono_color = "#ff007a" if is_damaged_nonmono else "#00f5a0"
            st.metric("6. Nonmonotonic Default Logic", results["nonmonotonic"], "Closed-world assumption")
            
        with st.expander("📋 Symbolic Telemetry Predicates (Facts Extracted)"):
            st.code("\n".join(facts), language="prolog")

with tab2:
    st.markdown("### 📊 Benchmark Comparison: 10 Standard Test Scenarios")
    st.markdown("Comparative matrix demonstrating where continuous probabilistic models diverge from discrete default logic.")
    
    rows = []
    for tc in TEST_CASES:
        res = evaluate_all_methods(tc)
        rows.append({
            "Case ID": tc["id"],
            "Weight Dev": f"{tc['weight_deviation_pct']}%",
            "Crack Sev": f"{tc['crack_severity_pct']}%",
            "Tilt Triggered": "YES" if tc["tilt_triggered"] else "NO",
            "Nonmonotonic": res["nonmonotonic"],
            "Bayes P(D)": f"{res['bayes']:.3f}",
            "CF Score": f"{res['cf']:+.3f}",
            "Bayes Net": f"{res['bn']:.3f}",
            "DS [Bel, Pl]": f"[{res['ds'][0]:.2f}, {res['ds'][1]:.2f}]",
            "Fuzzy": f"{res['fuzzy']:.1f}"
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem;">
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(0, 242, 254, 0.25); border-radius: 12px; padding: 1.2rem;">
            <div style="font-weight: 700; color: #00f2fe; margin-bottom: 6px;">⚡ Critical Divergence: Case TC-B3</div>
            <p style="color: #94a3b8; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                <b>Parameters:</b> Weight=70%, Crack=5%, Tilt=False.<br>
                <b>Resolution:</b> Nonmonotonic default logic asserts <i>NotDamaged</i> because weight alone doesn't trigger its rigid symbolic rule. However, continuous models (Bayes, CF, Fuzzy) reliably declare <i>Damaged</i> as 70% strain creates overwhelming probabilistic evidence.
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(121, 40, 202, 0.25); border-radius: 12px; padding: 1.2rem;">
            <div style="font-weight: 700; color: #b388ff; margin-bottom: 6px;">⚡ Critical Divergence: Case TC-B5</div>
            <p style="color: #94a3b8; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                <b>Parameters:</b> Weight=20%, Crack=10%, Tilt=True.<br>
                <b>Resolution:</b> Nonmonotonic logic instantly flags <i>Damaged</i> due to the discrete tilt rule. Fuzzy logic evaluates <i>NotDamaged</i> because its linguistic membership sets focus primarily on the low continuous strain and crack severity.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
