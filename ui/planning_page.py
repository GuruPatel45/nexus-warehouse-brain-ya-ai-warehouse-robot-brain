import json
import streamlit as st
from ui.theme import render_page_header, render_cyber_card
from modules.planning.state import WorldState, is_goal_satisfied
from modules.planning.goal_stack_planner import plan_goal_stack, _infer_towers
from modules.planning.nonlinear_planner import plan_nonlinear
from modules.planning.hierarchical import expand_load_pallet
from modules.planning.reactive import execute_with_reactive_layer

render_page_header(
    title="AUTONOMOUS TASK & MOTION PLANNING",
    subtitle="Neuro-symbolic block stacking, nonlinear partial-order planning, and real-time reactive disturbance recovery.",
    badge="MODULE A",
    icon="🏗️"
)

# Preset Scenarios
PRESETS = {
    "Classic 3-Block Stacking": {
        "start": {"on": {"B": "A", "A": "PALLET", "C": "PALLET"}, "holding": None},
        "goal": {"on": {"A": "B", "B": "C", "C": "PALLET"}},
        "dist": [{"after_step": 2, "type": "disturbance", "block": "A"}]
    },
    "High-Priority Inversion": {
        "start": {"on": {"C": "A", "A": "PALLET", "B": "PALLET"}, "holding": None},
        "goal": {"on": {"A": "B", "B": "C", "C": "PALLET"}},
        "dist": [{"after_step": 1, "type": "disturbance", "block": "C"}]
    },
    "Multi-Pallet Dispersion": {
        "start": {"on": {"A": "B", "B": "C", "C": "PALLET"}, "holding": None},
        "goal": {"on": {"A": "PALLET", "B": "PALLET", "C": "PALLET"}},
        "dist": []
    }
}

st.markdown("### 🎛️ Scenario Configuration")
col_preset, col_btn = st.columns([3, 1])
with col_preset:
    selected_preset = st.selectbox(
        "Load Autonomous Mission Profile",
        ["Classic 3-Block Stacking", "High-Priority Inversion", "Multi-Pallet Dispersion", "Custom Payload"]
    )

if selected_preset in PRESETS:
    default_start_val = json.dumps(PRESETS[selected_preset]["start"], indent=2)
    default_goal_val = json.dumps(PRESETS[selected_preset]["goal"], indent=2)
    default_dist_val = json.dumps(PRESETS[selected_preset]["dist"], indent=2)
else:
    default_start_val = json.dumps({"on": {"B": "A", "A": "PALLET", "C": "PALLET"}, "holding": None}, indent=2)
    default_goal_val = json.dumps({"on": {"A": "B", "B": "C", "C": "PALLET"}}, indent=2)
    default_dist_val = json.dumps([{"after_step": 2, "type": "disturbance", "block": "A"}], indent=2)

col1, col2 = st.columns(2)
with col1:
    start_json = st.text_area("Initial Spatial World State (JSON)", value=default_start_val, height=140)
with col2:
    goal_json = st.text_area("Target Spatial Goal State (JSON)", value=default_goal_val, height=140)

dist_json = st.text_area("Environmental Disturbances (Simulated Drops / Gripper Faults)", value=default_dist_val, height=90)

# Helper for rendering physical block towers
def render_block_tower(state_data, label):
    on_dict = state_data.get("on", {})
    holding = state_data.get("holding")
    
    html = f"""
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 12px; padding: 1rem; margin-top: 0.5rem;">
        <div style="font-weight: 700; font-size: 0.85rem; color: #00f2fe; text-transform: uppercase; margin-bottom: 0.8rem; letter-spacing: 0.05em;">{label}</div>
        <div style="display: flex; gap: 1.5rem; align-items: flex-end; justify-content: center; min-height: 120px; padding: 10px; border-bottom: 3px solid #7928ca;">
    """
    
    # Simple tower parser
    pallet_bases = [b for b, below in on_dict.items() if below == "PALLET"]
    for base in sorted(pallet_bases):
        # find tower up
        tower = [base]
        curr = base
        while True:
            above = [k for k, v in on_dict.items() if v == curr]
            if above:
                curr = above[0]
                tower.append(curr)
            else:
                break
        
        html += '<div style="display: flex; flex-direction: column-reverse; align-items: center; gap: 4px;">'
        colors = {"A": "#00f2fe", "B": "#7928ca", "C": "#00f5a0", "D": "#f59e0b", "E": "#ff007a"}
        for b in tower:
            c = colors.get(b, "#38bdf8")
            html += f"""
            <div style="width: 44px; height: 32px; background: rgba(15, 23, 42, 0.9); border: 2px solid {c}; 
                        box-shadow: 0 0 10px {c}44; border-radius: 6px; display: flex; align-items: center; 
                        justify-content: center; font-weight: 800; color: #ffffff; font-size: 0.95rem;">
                {b}
            </div>
            """
        html += '<div style="font-size: 0.7rem; color: #64748b; margin-top: 4px; font-weight: 600;">PALLET</div></div>'
    
    if holding:
        html += f"""
        <div style="display: flex; flex-direction: column; align-items: center; margin-left: 1rem;">
            <div style="font-size: 0.7rem; color: #f59e0b; font-weight: 700;">GRIPPER HOLD</div>
            <div style="width: 44px; height: 32px; background: rgba(245, 158, 11, 0.2); border: 2px dashed #f59e0b; 
                        border-radius: 6px; display: flex; align-items: center; justify-content: center; 
                        font-weight: 800; color: #ffffff; margin-top: 4px;">{holding}</div>
        </div>
        """
        
    html += """
        </div>
    </div>
    """
    return html

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

if st.button("🚀 SYNTHESIZE & EXECUTE ROBOTIC PLANS", type="primary", use_container_width=True):
    try:
        start_data = json.loads(start_json)
        goal_data = json.loads(goal_json)
        dist_data = json.loads(dist_json)
        start_state = WorldState(**start_data)
        
        # Render visual layout preview
        prev_col1, prev_col2 = st.columns(2)
        with prev_col1:
            st.markdown(render_block_tower(start_data, "Initial Physical Configuration"), unsafe_allow_html=True)
        with prev_col2:
            st.markdown(render_block_tower(goal_data, "Target Spatial Arrangement"), unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Goal Stack Planner", 
            "⚡ Nonlinear (POP)", 
            "🧩 Hierarchical (HTN)", 
            "🛡️ Reactive Fault Recovery"
        ])
        
        with tab1:
            st.markdown("#### 🎯 Linear Goal Stack Planning Engine")
            plan, trace = plan_goal_stack(start_state, goal_data)
            
            m_col1, m_col2 = st.columns([1, 3])
            with m_col1:
                st.metric(label="Sequential Actions", value=f"{len(plan)} Steps")
            with m_col2:
                # Render formatted plan cards
                steps_html = "<div style='display: flex; flex-direction: column; gap: 8px; margin-top: 0.5rem;'>"
                for idx, action in enumerate(plan):
                    act_name = action[0]
                    act_args = ", ".join(action[1:])
                    steps_html += f"""
                    <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(0, 242, 254, 0.25); border-left: 4px solid #00f2fe; border-radius: 8px; padding: 0.6rem 1rem; display: flex; align-items: center; justify-content: space-between;">
                        <span style="font-weight: 700; color: #00f2fe; font-family: 'Space Grotesk', monospace;">STEP {idx+1}</span>
                        <span style="font-weight: 700; color: #ffffff; font-family: 'JetBrains Mono', monospace;">{act_name}(<span style="color: #b388ff;">{act_args}</span>)</span>
                    </div>
                    """
                steps_html += "</div>"
                st.markdown(steps_html, unsafe_allow_html=True)
            
            with st.expander("🔍 Deep Goal-Stack Symbolic Trace", expanded=False):
                for line in trace:
                    st.text(line)
        
        with tab2:
            st.markdown("#### ⚡ Partial-Order Causal Link Planner (POP)")
            pop_plan = plan_nonlinear(start_state, goal_data)
            linear_seq = pop_plan.linearize()
            layers = pop_plan.parallel_steps()
            
            pop_col1, pop_col2 = st.columns(2)
            with pop_col1:
                st.metric(label="Linearized Sequence", value=f"{len(linear_seq)} Steps")
            with pop_col2:
                st.metric(label="Parallel Concurrency Layers", value=f"{len(layers)} Stages")
            
            st.markdown("##### 🔀 Concurrent Execution Stages:")
            for i, layer in enumerate(layers):
                stage_content = ", ".join([f"{a[0]}({', '.join(a[1:])})" for a in layer])
                st.markdown(f"""
                <div style="background: rgba(121, 40, 202, 0.15); border: 1px solid rgba(121, 40, 202, 0.4); border-radius: 10px; padding: 0.8rem 1.2rem; margin-bottom: 0.6rem; display: flex; align-items: center; justify-content: space-between;">
                    <span class="cyber-badge badge-purple">STAGE {i+1}</span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-weight: 600; color: #f8fafc;">{stage_content}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("#### 🧩 Hierarchical Task Network (HTN Decomposition)")
            towers = _infer_towers(goal_data)
            if towers:
                order = towers[0]
                expanded = expand_load_pallet(start_state, "P", order)
                st.info(f"Target Assembly Order: {order}")
                st.markdown("**Primitive Actuator Operators:**")
                for act in expanded:
                    st.code(f"EXECUTE: {act[0]}({', '.join(act[1:])})", language="bash")
            else:
                st.warning("No structured tower configurations inferred.")
                
        with tab4:
            st.markdown("#### 🛡️ Closed-Loop Reactive Controller")
            result = execute_with_reactive_layer(plan, start_state, dist_data)
            
            if result["reactive_log"]:
                for line in result["reactive_log"]:
                    st.markdown(f"""
                    <div style="background: rgba(255, 0, 122, 0.15); border: 1px solid rgba(255, 0, 122, 0.4); border-radius: 10px; padding: 0.8rem 1.2rem; margin-bottom: 0.6rem;">
                        <span style="color: #ff007a; font-weight: 800;">⚡ CONTINGENCY DETECTED:</span> {line}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ Nominal Execution: No unforeseen disturbances breached preconditions.")
            
            sat = is_goal_satisfied(result['final_state'], goal_data)
            if sat:
                st.markdown("""
                <div style="background: rgba(0, 245, 160, 0.15); border: 1px solid rgba(0, 245, 160, 0.4); border-radius: 10px; padding: 1rem; margin-top: 1rem; text-align: center;">
                    <span style="color: #00f5a0; font-weight: 800; font-size: 1.1rem;">🎯 GOAL FULLY RECOVERED & SATISFIED</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Physical goal was not satisfied.")
                
    except Exception as e:
        st.error(f"Execution Error: {e}")
