import json
import streamlit as st
from modules.planning.state import WorldState, is_goal_satisfied
from modules.planning.goal_stack_planner import plan_goal_stack
from modules.planning.nonlinear_planner import plan_nonlinear
from modules.planning.hierarchical import expand_load_pallet
from modules.planning.reactive import execute_with_reactive_layer

st.title("🏗️ Planning (Module A)")
st.write("Plan stacking sequences using different approaches: Goal Stack, Nonlinear (POP), Hierarchical, and Reactive.")

st.sidebar.header("Scenario Configuration")
default_start = json.dumps({"on": {"B": "A", "A": "PALLET", "C": "PALLET"}, "holding": None}, indent=2)
default_goal = json.dumps({"on": {"A": "B", "B": "C", "C": "PALLET"}}, indent=2)
default_disturbance = json.dumps([{"after_step": 2, "type": "disturbance", "block": "A"}], indent=2)

col1, col2 = st.columns(2)
with col1:
    start_json = st.text_area("Start State (JSON)", value=default_start, height=150)
with col2:
    goal_json = st.text_area("Goal State (JSON)", value=default_goal, height=150)

dist_json = st.text_area("Disturbances (JSON, for Reactive Planning)", value=default_disturbance, height=100)

if st.button("Run Planners", type="primary"):
    try:
        start_data = json.loads(start_json)
        goal_data = json.loads(goal_json)
        dist_data = json.loads(dist_json)
        
        start_state = WorldState(**start_data)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Goal Stack", "Nonlinear (POP)", "Hierarchical", "Reactive"])
        
        with tab1:
            st.subheader("Goal Stack Planning")
            st.text(f"Start: {start_state}\nGoal: {goal_data}")
            plan, trace = plan_goal_stack(start_state, goal_data)
            st.success(f"Plan found: {len(plan)} steps")
            st.write(plan)
            with st.expander("Execution Trace"):
                for line in trace:
                    st.text(line)
        
        with tab2:
            st.subheader("Nonlinear Planning")
            pop_plan = plan_nonlinear(start_state, goal_data)
            linear_seq = pop_plan.linearize()
            layers = pop_plan.parallel_steps()
            st.success(f"Linearized plan: {len(linear_seq)} steps")
            st.write(linear_seq)
            st.markdown("**Parallel Executable Layers:**")
            for i, layer in enumerate(layers):
                st.info(f"Layer {i+1}: {layer}")
                
        with tab3:
            st.subheader("Hierarchical Planning")
            st.write("Expanding high-level `LoadPallet(P)` operator into primitive actions.")
            from modules.planning.goal_stack_planner import _infer_towers
            towers = _infer_towers(goal_data)
            if towers:
                order = towers[0]
                expanded = expand_load_pallet(start_state, "P", order)
                st.write(f"Inferred order: {order}")
                st.write(expanded)
            else:
                st.write("No towers inferred from goal state.")
            
        with tab4:
            st.subheader("Reactive Execution")
            st.write("Simulating execution of the Goal Stack plan with disturbances.")
            result = execute_with_reactive_layer(plan, start_state, dist_data)
            st.markdown("**Reactive Log:**")
            for line in result["reactive_log"]:
                st.warning(line)
            with st.expander("Execution Trace"):
                for line in result["trace"]:
                    st.text(line)
            st.write(f"**Final state:** {result['final_state']}")
            sat = is_goal_satisfied(result['final_state'], goal_data)
            if sat:
                st.success("Goal satisfied successfully despite disturbances!")
            else:
                st.error("Goal not satisfied.")
                
    except Exception as e:
        st.error(f"Error parsing JSON or executing plan: {e}")
