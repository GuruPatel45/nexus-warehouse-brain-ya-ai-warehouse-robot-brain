import streamlit as st
from ui.theme import render_page_header, render_cyber_card
from modules.expert_system.rule_engine import diagnose, _load_rules
from modules.expert_system.knowledge_acquisition import append_rule

render_page_header(
    title="AI HARDWARE DIAGNOSTIC SURGEON",
    subtitle="Forward-chaining symbolic expert system evaluating AGV electromechanical telemetry, with explanation trace & knowledge acquisition.",
    badge="MODULE E",
    icon="🛠️"
)

tab1, tab2, tab3 = st.tabs([
    "🩺 Interactive Diagnostic Triage", 
    "✍️ Knowledge Acquisition Studio", 
    "📚 Live Rule Base Repository"
])

rules = _load_rules()

with tab1:
    st.markdown("### 🎛️ Symptom Observation Matrix")
    st.markdown("Tag active sensor anomalies and physical telemetry flags observed across the AGV chassis.")
    
    # Extract unique IF-facts from rules
    all_symptoms = set()
    for rule in rules:
        for f in rule["if"]:
            if not f.startswith("diagnosis:"):
                all_symptoms.add(f)
                
    selected_symptoms = set()
    
    # Render symptoms in organized columns with styled cards
    cols = st.columns(3)
    sorted_syms = sorted(all_symptoms)
    
    for i, symptom in enumerate(sorted_syms):
        target_col = cols[i % 3]
        clean_name = symptom.replace("symptom:", "").replace("_", " ").upper()
        with target_col:
            if st.checkbox(f"🔴 {clean_name}", key=f"sym_{symptom}"):
                selected_symptoms.add(symptom)
                
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    if st.button("⚡ EXECUTE FORWARD-CHAINING DIAGNOSTIC ENGINE", type="primary", use_container_width=True):
        if not selected_symptoms:
            st.warning("⚠️ Please select at least one symptom indicator to initialize forward-chaining.")
        else:
            result = diagnose(selected_symptoms)
            diagnoses = result["diagnoses"]
            
            if diagnoses:
                for d in diagnoses:
                    clean_diag = d.replace("diagnosis:", "").replace("_", " ").upper()
                    st.markdown(f"""
                    <div style="background: rgba(255, 0, 122, 0.15); border: 2px solid #ff007a; border-radius: 14px; 
                                padding: 1.25rem 1.75rem; margin: 1.25rem 0; box-shadow: 0 0 25px rgba(255, 0, 122, 0.3);
                                display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                        <div>
                            <div style="font-size: 0.75rem; color: #ff007a; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase;">
                                CRITICAL HARDWARE FAULT IDENTIFIED
                            </div>
                            <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin-top: 4px;">
                                🚨 {clean_diag}
                            </div>
                        </div>
                        <div class="cyber-badge badge-rose" style="font-size: 0.85rem; padding: 6px 16px;">
                            INTERVENE IMMEDIATELY
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: rgba(0, 245, 160, 0.12); border: 2px solid #00f5a0; border-radius: 14px; 
                            padding: 1.25rem 1.75rem; margin: 1.25rem 0; text-align: center;">
                    <div style="color: #00f5a0; font-weight: 800; font-size: 1.2rem;">
                        ✅ NO FAULT DETECTED // HARDWARE WITHIN SPECIFICATION
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("#### 🔍 Symbolic Explanation Trace (Inference Tree)")
            if result["trace"]:
                trace_html = "<div style='display: flex; flex-direction: column; gap: 10px; margin-top: 0.5rem;'>"
                for rid, expl, then_fact in result["trace"]:
                    trace_html += f"""
                    <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(0, 242, 254, 0.2); border-left: 4px solid #7928ca; border-radius: 8px; padding: 0.8rem 1.2rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <span class="cyber-badge badge-purple">RULE {rid} FIRED</span>
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #00f5a0;">+ INFERRED: {then_fact}</span>
                        </div>
                        <div style="color: #cbd5e1; font-size: 0.9rem;">{expl}</div>
                    </div>
                    """
                trace_html += "</div>"
                st.markdown(trace_html, unsafe_allow_html=True)
            else:
                st.info("No inference rules triggered with the given symptom set.")
                
            with st.expander("💾 Working Memory Final State"):
                st.json(list(result["working_memory"]))

with tab2:
    st.markdown("### ✍️ Zero-Downtime Knowledge Acquisition")
    st.markdown("Inject new production rules into the expert system dynamically without restarting services.")
    
    with st.form("new_rule_form"):
        r_id = st.text_input("Unique Rule Identifier (e.g. R99, R102)")
        r_if = st.text_input("IF Conditions (comma-separated, e.g. symptom:bearing_noise, symptom:high_temp)")
        r_not = st.text_input("NOT Negative Conditions (optional comma-separated)")
        r_then = st.text_input("THEN Fact Inferred (e.g. diagnosis:bearing_spalling)")
        r_exp = st.text_area("Human-Readable Engineering Rationale / Explanation")
        
        submitted = st.form_submit_button("⚡ COMPILE & INJECT RULE INTO KNOWLEDGE BASE")
        if submitted:
            if r_id and r_if and r_then:
                new_rule = {
                    "id": r_id.strip(),
                    "if": [x.strip() for x in r_if.split(",") if x.strip()],
                    "not": [x.strip() for x in r_not.split(",") if x.strip()] if r_not else [],
                    "then": r_then.strip(),
                    "explanation": r_exp.strip()
                }
                append_rule(new_rule)
                st.success(f"✅ Rule `{r_id}` successfully validated and appended to `rules.json`!")
                st.rerun()
            else:
                st.error("Rule ID, IF conditions, and THEN fact are required.")

with tab3:
    st.markdown("### 📚 Compiled Diagnostic Rule Base")
    st.markdown(f"Currently indexing **{len(rules)} production rules** across drivetrain, sensory, and electrical domains.")
    
    for r in rules:
        with st.expander(f"🔹 [{r['id']}] {r['explanation']}"):
            st.markdown(f"""
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; line-height: 1.6; color: #f8fafc;">
                <b style="color: #00f2fe;">IF</b> {r['if']}<br>
                <b style="color: #ff007a;">NOT</b> {r.get('not', [])}<br>
                <b style="color: #00f5a0;">THEN</b> {r['then']}
            </div>
            """, unsafe_allow_html=True)
