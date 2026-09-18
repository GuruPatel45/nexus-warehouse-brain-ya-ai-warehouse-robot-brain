import streamlit as st
import matplotlib.pyplot as plt
from modules.game.dock_game import simulate_dock_game
from modules.game.benchmark_chart import run_benchmark, DEPTHS

st.title("🎮 Dock Game (Module C)")
st.write("Adversarial search for dock contention. Robot A vs Robot B competing for the charging dock.")

tab1, tab2 = st.tabs(["Playable Simulation", "Algorithm Benchmarks"])

with tab1:
    st.subheader("Simulate Game")
    col1, col2 = st.columns(2)
    with col1:
        depth = st.slider("Search Depth", 1, 6, 3)
    with col2:
        opponent = st.selectbox("Opponent (R2)", ["random", "self"])
        
    if st.button("Run Simulation", type="primary"):
        with st.spinner("Simulating..."):
            result = simulate_dock_game(depth=depth, opponent=opponent)
            st.success(f"Game over after {result['plies']} plies. Winner: **{result['winner']}**")
            
            with st.expander("View Move History and Board States", expanded=True):
                for entry in result["trace"]:
                    st.text(entry)

with tab2:
    st.subheader("Algorithm Benchmarks (Nodes Explored)")
    st.write("Comparing MiniMax, AlphaBeta, and Iterative Deepening.")
    
    @st.cache_data
    def get_benchmark_data():
        return run_benchmark()
        
    if st.button("Generate Benchmark Chart"):
        with st.spinner("Running search algorithms up to depth 6 (this may take a moment)..."):
            data = get_benchmark_data()
            
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(DEPTHS, data["minimax"], "o-", color="#e74c3c", linewidth=2, markersize=7, label="MiniMax")
            ax.plot(DEPTHS, data["alphabeta"], "s-", color="#3498db", linewidth=2, markersize=7, label="AlphaBeta")
            ax.plot(DEPTHS, data["ids"], "^-", color="#2ecc71", linewidth=2, markersize=7, label="AlphaBeta+IDS")
            ax.set_xlabel("Search Depth")
            ax.set_ylabel("Nodes Visited")
            ax.set_title("Dock Contention: Nodes Explored vs. Depth")
            ax.legend()
            ax.grid(True, linestyle="--", alpha=0.6)
            ax.set_yscale("log")
            
            # Transparent background for dark mode compatibility
            fig.patch.set_alpha(0)
            ax.set_facecolor('none')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            ax.tick_params(colors='white')
            
            st.pyplot(fig)
            
            st.markdown("""
            **Analysis:**
            - **Alpha-Beta Pruning** significantly reduces the number of nodes visited compared to plain **MiniMax**.
            - **Iterative Deepening Search (IDS)** adds a small overhead for shallow searches but allows for time-limited deep searches and better move ordering in complex games.
            """)
