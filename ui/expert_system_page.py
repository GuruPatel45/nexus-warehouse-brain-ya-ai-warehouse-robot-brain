import streamlit as st
from modules.expert_system.rule_engine import diagnose, _load_rules
from modules.expert_system.knowledge_acquisition import append_rule

st.title("🛠️ Maintenance Expert (Module E)")
st.write("Rule-based forward-chaining expert system for warehouse maintenance diagnostics.")

tab1, tab2, tab3 = st.tabs(["Interactive Diagnosis", "Knowledge Acquisition", "View Rules"])

rules = _load_rules()

with tab1:
    st.subheader("Interactive Diagnosis")
    st.write("Select the symptoms you are observing in the warehouse robot:")
    
    # Extract unique IF-facts from rules
    all_symptoms = set()
    for rule in rules:
        for f in rule["if"]:
            if not f.startswith("diagnosis:"):
                all_symptoms.add(f)
                
    selected_symptoms = set()
    col1, col2 = st.columns(2)
    
    for i, symptom in enumerate(sorted(all_symptoms)):
        target_col = col1 if i % 2 == 0 else col2
        if target_col.checkbox(symptom, key=f"sym_{symptom}"):
            selected_symptoms.add(symptom)
            
    if st.button("Run Diagnostic Engine", type="primary"):
        if not selected_symptoms:
            st.warning("Please select at least one symptom.")
        else:
            result = diagnose(selected_symptoms)
            st.markdown("### Diagnosis")
            if result["diagnoses"]:
                for d in result["diagnoses"]:
                    st.error(f"**{d.replace('diagnosis:', '').replace('_', ' ').upper()}**")
            else:
                st.success("**NO FAULT DETECTED** based on current rules.")
                
            st.markdown("### Explanation Trace")
            for rid, expl, then_fact in result["trace"]:
                st.info(f"**Rule {rid} fired:** {expl} ➡️ Added fact: `{then_fact}`")
            
            with st.expander("Working Memory State"):
                st.write(result["working_memory"])

with tab2:
    st.subheader("Knowledge Acquisition")
    st.write("Add a new rule to the expert system without modifying code.")
    
    with st.form("new_rule_form"):
        r_id = st.text_input("Rule ID (e.g. R99)")
        r_if = st.text_input("IF conditions (comma-separated, e.g. symptom:motor_hot)")
        r_not = st.text_input("NOT conditions (comma-separated, optional)")
        r_then = st.text_input("THEN fact (e.g. diagnosis:motor_fault)")
        r_exp = st.text_input("Explanation")
        
        submitted = st.form_submit_button("Add Rule")
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
                st.success(f"Rule {r_id} successfully added to `rules.json`!")
                st.rerun()
            else:
                st.error("Rule ID, IF conditions, and THEN fact are required.")

with tab3:
    st.subheader("Current Rule Base")
    for r in rules:
        with st.expander(f"{r['id']}: {r['explanation']}"):
            st.code(f"IF {r['if']}\nNOT {r.get('not', [])}\nTHEN {r['then']}")
