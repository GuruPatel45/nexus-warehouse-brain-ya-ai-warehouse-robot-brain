import json
import streamlit as st
from ui.theme import render_page_header, render_cyber_card, render_html
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
    
    # 1. Infer all blocks
    all_blocks = set(on_dict.keys()) | {v for v in on_dict.values() if v and v != "PALLET"}
    
    # 2. A block is a base if it rests on PALLET or is not on any other block
    bases = [b for b in all_blocks if on_dict.get(b) == "PALLET" or b not in on_dict]
    if not bases and all_blocks:
        bases = list(all_blocks)
        
    towers = []
    for base in sorted(bases):
        tower = [base]
        curr = base
        while True:
            above = [k for k, v in on_dict.items() if v == curr]
            if above:
                curr = above[0]
                tower.append(curr)
            else:
                break
        towers.append(tower)
        
    colors = {"A": "#00f2fe", "B": "#b388ff", "C": "#00f5a0", "D": "#f59e0b", "E": "#ff007a"}
    
    tower_elements = []
    for tower in towers:
        blocks_top_down = list(reversed(tower))
        b_html = []
        for b in blocks_top_down:
            c = colors.get(b, "#38bdf8")
            b_html.append(
                f'<div style="width: 54px; height: 38px; background: rgba(15, 23, 42, 0.95); border: 2px solid {c}; '
                f'box-shadow: 0 0 14px {c}55; border-radius: 7px; display: flex; align-items: center; '
                f'justify-content: center; font-weight: 800; color: #ffffff; font-size: 1.1rem; font-family: sans-serif;">{b}</div>'
            )
        b_str = "".join(b_html)
        tower_elements.append(
            f'<div style="display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 5px;">'
            f'{b_str}'
            f'<div style="width: 68px; height: 8px; background: linear-gradient(90deg, #334155, #64748b, #334155); border-radius: 3px; margin-top: 3px;"></div>'
            f'<div style="font-size: 0.65rem; color: #94a3b8; font-weight: 700; letter-spacing: 0.05em; margin-top: 2px;">PALLET</div>'
            f'</div>'
        )
    
    towers_combined = "".join(tower_elements)
    
    holding_html = ""
    if holding:
        c = colors.get(holding, "#f59e0b")
        holding_html = (
            f'<div style="display: flex; flex-direction: column; align-items: center; margin-left: 1.5rem; align-self: flex-start;">'
            f'<div style="font-size: 0.7rem; color: #f59e0b; font-weight: 800; letter-spacing: 0.05em; margin-bottom: 4px;">⚡ GRIPPER</div>'
            f'<div style="width: 54px; height: 38px; background: rgba(245, 158, 11, 0.2); border: 2px dashed #f59e0b; '
            f'border-radius: 7px; display: flex; align-items: center; justify-content: center; '
            f'font-weight: 800; color: #ffffff; font-size: 1.1rem; box-shadow: 0 0 12px rgba(245, 158, 11, 0.35);">{holding}</div>'
            f'</div>'
        )
        
    full_html = (
        f'<div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(0, 242, 254, 0.25); border-radius: 14px; padding: 1.2rem; margin-top: 0.5rem; box-shadow: 0 8px 25px rgba(0,0,0,0.4);">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">'
        f'<div style="font-weight: 700; font-size: 0.85rem; color: #00f2fe; text-transform: uppercase; letter-spacing: 0.06em;">{label}</div>'
        f'<div style="font-size: 0.75rem; color: #94a3b8;">{len(towers)} Tower Stack(s)</div>'
        f'</div>'
        f'<div style="display: flex; gap: 2rem; align-items: flex-end; justify-content: center; min-height: 150px; padding: 15px 10px 10px 10px; border-bottom: 3px solid #00f2fe; background: radial-gradient(circle at 50% 100%, rgba(0, 242, 254, 0.08) 0%, transparent 70%);">'
        f'{towers_combined}{holding_html}'
        f'</div></div>'
    )
    return full_html

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

if st.button("🚀 SYNTHESIZE & EXECUTE ROBOTIC PLANS", type="primary"):
    try:
        start_data = json.loads(start_json)
        goal_data = json.loads(goal_json)
        dist_data = json.loads(dist_json)
        start_state = WorldState(**start_data)
        
        # Render visual layout preview
        prev_col1, prev_col2 = st.columns(2)
        with prev_col1:
            render_html(render_block_tower(start_data, "Initial Physical Configuration"))
        with prev_col2:
            render_html(render_block_tower(goal_data, "Target Spatial Arrangement"))
        
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
                # Render formatted plan cards with operator icons
                op_icons = {"UNSTACK": "📤", "STACK": "📥", "PICKUP": "🦾", "PUTDOWN": "📦"}
                step_cards = []
                for idx, action in enumerate(plan):
                    act_name = action[0]
                    act_args = ", ".join(action[1:])
                    icon = op_icons.get(act_name, "⚡")
                    step_cards.append(
                        f'<div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0, 242, 254, 0.25); border-left: 4px solid #00f2fe; border-radius: 8px; padding: 0.65rem 1.1rem; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">'
                        f'<div style="display: flex; align-items: center; gap: 10px;">'
                        f'<span style="font-size: 1.1rem;">{icon}</span>'
                        f'<span style="font-weight: 700; color: #00f2fe; font-size: 0.85rem;">STEP {idx+1}</span>'
                        f'</div>'
                        f'<span style="font-weight: 700; color: #ffffff; font-family: monospace; font-size: 0.95rem;">{act_name}(<span style="color: #b388ff;">{act_args}</span>)</span>'
                        f'</div>'
                    )
                steps_html = f'<div style="display: flex; flex-direction: column; gap: 8px; margin-top: 0.5rem;">{"".join(step_cards)}</div>'
                render_html(steps_html)
            
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
            stage_htmls = []
            for i, layer in enumerate(layers):
                stage_content = ", ".join([f"{a[0]}({', '.join(a[1:])})" for a in layer])
                stage_htmls.append(
                    f'<div style="background: rgba(121, 40, 202, 0.15); border: 1px solid rgba(121, 40, 202, 0.4); border-radius: 10px; padding: 0.8rem 1.2rem; margin-bottom: 0.6rem; display: flex; align-items: center; justify-content: space-between;">'
                    f'<span class="cyber-badge badge-purple">STAGE {i+1}</span>'
                    f'<span style="font-family: monospace; font-weight: 600; color: #f8fafc;">{stage_content}</span>'
                    f'</div>'
                )
            render_html("".join(stage_htmls))
        
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
                    render_html(
                        f'<div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b; border-radius: 10px; padding: 0.8rem 1.2rem; margin-bottom: 0.6rem;">'
                        f'<b style="color: #f59e0b;">🛡️ REACTIVE REPAIR APPLIED:</b> <span style="color: #f8fafc;">{line}</span>'
                        f'</div>'
                    )
            else:
                st.success("✅ Nominal Execution: No unforeseen disturbances breached preconditions.")
            
            sat = is_goal_satisfied(result['final_state'], goal_data)
            if sat:
                render_html(
                    '<div style="background: rgba(0, 245, 160, 0.15); border: 1px solid rgba(0, 245, 160, 0.4); border-radius: 10px; padding: 1rem; margin-top: 1rem; text-align: center;">'
                    '<span style="color: #00f5a0; font-weight: 800; font-size: 1.1rem;">🎯 GOAL FULLY RECOVERED & SATISFIED DESPITE SIMULATED DISTURBANCE</span>'
                    '</div>'
                )
            else:
                st.error("❌ Physical goal was not satisfied.")
                
    except Exception as e:
        st.error(f"Execution Error: {e}")
