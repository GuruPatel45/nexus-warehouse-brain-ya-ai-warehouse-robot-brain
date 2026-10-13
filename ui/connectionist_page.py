import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from ui.theme import render_page_header, render_cyber_card
from modules.connectionist.hopfield import (
    generate_pattern_1, generate_pattern_2, generate_pattern_3,
    generate_pattern_4, generate_pattern_5, generate_pattern_6,
    train, corrupt, energy
)
from modules.connectionist.rnn_model import generate_synthetic_sequences, train_rnn

render_page_header(
    title="NEURAL CONNECTIONIST & TEMPORAL AI",
    subtitle="Associative attractor Hopfield memory for damaged pallet barcode recall and recurrent temporal drift anomaly detection.",
    badge="MODULE D",
    icon="🧠"
)

tab1, tab2, tab3 = st.tabs([
    "🧩 Hopfield Associative Memory", 
    "📈 RNN Temporal Sequence Classifier", 
    "⚖️ Connectionist Architecture Matrix"
])

def render_led_matrix(pattern, title, color="#00f2fe"):
    """Render a 5x5 pattern as an illuminated cyber LED grid."""
    matrix = pattern.reshape(5, 5)
    html = f"""
    <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
        <div style="font-size: 0.8rem; font-weight: 700; color: {color}; margin-bottom: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">{title}</div>
        <div style="display: grid; grid-template-columns: repeat(5, 28px); gap: 5px; justify-content: center; margin: 0 auto;">
    """
    for r in range(5):
        for c in range(5):
            val = matrix[r, c]
            if val == 1:
                html += f"""<div style="width: 28px; height: 28px; background: {color}; border-radius: 4px; box-shadow: 0 0 10px {color};"></div>"""
            else:
                html += """<div style="width: 28px; height: 28px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255,255,255,0.05); border-radius: 4px;"></div>"""
    html += """
        </div>
    </div>
    """
    return html

with tab1:
    st.markdown("### 🧩 Hopfield Network: Content-Addressable Memory")
    st.markdown("Recovers degraded or partially obscured optical pallet identifiers (5×5 bipolar spatial memories) by settling into minimal energy attractors.")
    
    patterns = [
        generate_pattern_1(), generate_pattern_2(), generate_pattern_3(),
        generate_pattern_4(), generate_pattern_5(), generate_pattern_6()
    ]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_idx = st.selectbox(
            "Target Prototype Pattern", 
            range(len(patterns)), 
            format_func=lambda i: f"Warehouse Identifier #{i+1}"
        )
        flip_frac = st.slider("Optical Noise / Bit Corruption (%)", 0, 50, 20) / 100.0
        
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    
    if st.button("⚡ EXECUTE ATTRACTOR RECALL & SETTLING", type="primary", use_container_width=True):
        W = train(patterns)
        original = patterns[selected_idx]
        corrupted = corrupt(original, flip_frac)
        
        # Track energy over iterations
        state = corrupted.copy()
        energies = [energy(W, state)]
        
        recovered = state.copy()
        n_features = len(recovered)
        for _ in range(100):
            changed = False
            indices = np.random.permutation(n_features)
            for i in indices:
                old_val = recovered[i]
                net_input = np.dot(W[i, :], recovered)
                new_val = 1 if net_input >= 0 else -1
                if new_val != old_val:
                    recovered[i] = new_val
                    changed = True
            energies.append(energy(W, recovered))
            if not changed:
                break
                
        # Show LED Grids
        colA, colB, colC = st.columns(3)
        with colA:
            st.markdown(render_led_matrix(original, "1. Ground Truth Prototype", "#00f2fe"), unsafe_allow_html=True)
        with colB:
            st.markdown(render_led_matrix(corrupted, f"2. Corrupted Sensor Input ({int(flip_frac*100)}% Noise)", "#ff007a"), unsafe_allow_html=True)
        with colC:
            st.markdown(render_led_matrix(recovered, "3. Attractor State Reconstructed", "#00f5a0"), unsafe_allow_html=True)
            
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("#### 📉 Lyapunov Energy Function Minimization")
        
        fig_e, ax_e = plt.subplots(figsize=(8, 3))
        ax_e.plot(energies, 'o-', color='#00f5a0', linewidth=2.5, markersize=7)
        ax_e.fill_between(range(len(energies)), energies, min(energies) - 5, color='#00f5a0', alpha=0.1)
        ax_e.set_xlabel("Settling Step (Iteration)", fontsize=10, fontweight='bold', color='#cbd5e1')
        ax_e.set_ylabel("Hopfield Energy E(x)", fontsize=10, fontweight='bold', color='#cbd5e1')
        ax_e.set_title("Convergence into Stable Attractor Basin", fontsize=11, fontweight='bold', color='#ffffff')
        ax_e.tick_params(colors='#94a3b8')
        ax_e.grid(True, linestyle="--", alpha=0.2, color='#64748b')
        fig_e.patch.set_alpha(0)
        ax_e.set_facecolor('#07090e')
        for spine in ax_e.spines.values():
            spine.set_color('#334155')
        st.pyplot(fig_e)

with tab2:
    st.markdown("### 📈 PyTorch Recurrent Neural Network (RNN)")
    st.markdown("Temporal pattern analysis detecting continuous mechanical degradation and sensor drift over 10-step telemetry windows.")
    
    col1, col2 = st.columns(2)
    with col1:
        epochs = st.number_input("Optimization Epochs", 1, 50, 15)
    with col2:
        hidden_size = st.number_input("Hidden Recurrent Units", 8, 128, 32)
        
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    
    if st.button("🚀 TRAIN & DEPLOY TEMPORAL RNN DETECTOR", type="primary", use_container_width=True):
        with st.spinner("Synthesizing telemetry streams and fitting PyTorch RNN..."):
            X, y = generate_synthetic_sequences(n=600, seq_len=10)
            model, train_losses = train_rnn(X, y, hidden_size=hidden_size, epochs=epochs, lr=0.01)
            
            st.markdown(f"""
            <div style="background: rgba(0, 245, 160, 0.12); border: 1px solid rgba(0, 245, 160, 0.4); 
                        border-radius: 12px; padding: 1rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #00f5a0; font-weight: 800; font-size: 1.05rem;">✅ Model Convergence Achieved across {epochs} Epochs</span>
                <span class="cyber-badge badge-emerald">FINAL LOSS: {train_losses[-1]:.4f}</span>
            </div>
            """, unsafe_allow_html=True)
            
            fig, ax = plt.subplots(figsize=(8, 3.2))
            ax.plot(train_losses, '-', color='#00f2fe', linewidth=2.5)
            ax.fill_between(range(len(train_losses)), train_losses, 0, color='#00f2fe', alpha=0.15)
            ax.set_title("Cross-Entropy Loss Trajectory", fontsize=11, fontweight='bold', color='#ffffff')
            ax.set_xlabel("Epoch", fontsize=10, fontweight='bold', color='#cbd5e1')
            ax.set_ylabel("Loss", fontsize=10, fontweight='bold', color='#cbd5e1')
            ax.tick_params(colors='#94a3b8')
            ax.grid(True, linestyle="--", alpha=0.2, color='#64748b')
            fig.patch.set_alpha(0)
            ax.set_facecolor('#07090e')
            for spine in ax.spines.values():
                spine.set_color('#334155')
            st.pyplot(fig)

with tab3:
    st.markdown("""
    ### ⚖️ Architectural Divergence: Static Attractors vs. Temporal Recurrence
    
    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 14px; padding: 1.5rem; margin-top: 1rem;">
        <table style="width: 100%; border-collapse: collapse; color: #f8fafc; font-size: 0.95rem;">
            <thead>
                <tr style="border-bottom: 2px solid rgba(0, 242, 254, 0.3); text-align: left;">
                    <th style="padding: 12px; color: #00f2fe;">Architectural Dimension</th>
                    <th style="padding: 12px; color: #b388ff;">Hopfield Attractor Network</th>
                    <th style="padding: 12px; color: #00f5a0;">Recurrent Neural Network (RNN)</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                    <td style="padding: 12px; font-weight: 700; color: #94a3b8;">Primary Function</td>
                    <td style="padding: 12px;">Associative, content-addressable memory retrieval.</td>
                    <td style="padding: 12px;">Temporal sequence classification and forecasting.</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                    <td style="padding: 12px; font-weight: 700; color: #94a3b8;">Data Domain</td>
                    <td style="padding: 12px;">Static spatial bit patterns (e.g., damaged QR / barcode).</td>
                    <td style="padding: 12px;">Time-series telemetry streams over temporal windows.</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                    <td style="padding: 12px; font-weight: 700; color: #94a3b8;">Theoretical Limitation</td>
                    <td style="padding: 12px;">Capacity capped at ~0.138N patterns; spurious minima risk.</td>
                    <td style="padding: 12px;">Vanishing / exploding gradients over long horizons.</td>
                </tr>
                <tr>
                    <td style="padding: 12px; font-weight: 700; color: #94a3b8;">Warehouse Utility</td>
                    <td style="padding: 12px;">Optical ID reconstruction when tags are scratched or scuffed.</td>
                    <td style="padding: 12px;">Detecting slow motor bearing overheating or wheel slip drift.</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
