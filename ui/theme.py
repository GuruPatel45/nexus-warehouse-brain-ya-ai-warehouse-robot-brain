"""
ui/theme.py
Comprehensive design system and styling engine for the Cyber-Warehouse Autonomous Brain.
Provides glassmorphism, cyber-industrial aesthetics, neon glowing accents,
custom typography, and helper layout components.
"""

import streamlit as st
import os

CYBER_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
/* ====== ROOT VARIABLES & THEME TOKENS ====== */
:root {
    --bg-primary: #07090e;
    --bg-secondary: #0d131f;
    --bg-card: rgba(15, 23, 42, 0.72);
    --bg-card-hover: rgba(22, 33, 62, 0.85);
    --border-glass: rgba(0, 242, 254, 0.18);
    --border-glass-hover: rgba(0, 242, 254, 0.45);
    
    --neon-cyan: #00f2fe;
    --neon-violet: #8a2be2;
    --neon-purple: #7928ca;
    --neon-emerald: #00f5a0;
    --neon-amber: #f59e0b;
    --neon-rose: #ff007a;
    
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    
    --glow-cyan: 0 0 20px rgba(0, 242, 254, 0.35);
    --glow-violet: 0 0 20px rgba(138, 43, 226, 0.35);
}

/* ====== GLOBAL PAGE STYLING ====== */
html, body, [class*="css"] {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background-color: var(--bg-primary) !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(121, 40, 202, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(0, 242, 254, 0.15) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(0, 245, 160, 0.08) 0px, transparent 50%) !important;
    background-attachment: fixed !important;
    color: var(--text-primary) !important;
}

/* Code & monospace */
code, pre, .stCodeBlock {
    font-family: 'JetBrains Mono', monospace !important;
    border-radius: 10px !important;
}

/* ====== CUSTOM SCROLLBAR ====== */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #090d16;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00f2fe 0%, #7928ca 100%);
    border-radius: 4px;
}

/* ====== SIDEBAR STYLING ====== */
[data-testid="stSidebar"] {
    background: rgba(10, 15, 26, 0.95) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(0, 242, 254, 0.12) !important;
}

[data-testid="stSidebarNav"] {
    padding-top: 1rem;
}

[data-testid="stSidebarNav"] span {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500;
    color: var(--text-secondary) !important;
}

[data-testid="stSidebarNav"] a:hover span,
[data-testid="stSidebarNav"] a[aria-current="page"] span {
    color: var(--neon-cyan) !important;
    text-shadow: 0 0 10px rgba(0, 242, 254, 0.4);
}

/* ====== BUTTONS ====== */
.stButton > button {
    background: linear-gradient(135deg, rgba(0, 242, 254, 0.15) 0%, rgba(121, 40, 202, 0.25) 100%) !important;
    border: 1px solid rgba(0, 242, 254, 0.4) !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    padding: 0.55rem 1.4rem !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #00f2fe 0%, #7928ca 100%) !important;
    border-color: #00f2fe !important;
    color: #050811 !important;
    font-weight: 700 !important;
    box-shadow: 0 0 25px rgba(0, 242, 254, 0.5), 0 0 40px rgba(121, 40, 202, 0.3) !important;
    transform: translateY(-2px) scale(1.01) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00f2fe 0%, #7928ca 100%) !important;
    color: #050811 !important;
    border: none !important;
    font-weight: 700 !important;
    box-shadow: 0 0 20px rgba(0, 242, 254, 0.4) !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 35px rgba(0, 242, 254, 0.7), 0 0 50px rgba(121, 40, 202, 0.5) !important;
    transform: translateY(-2px) scale(1.02) !important;
}

/* ====== TABS ====== */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15, 23, 42, 0.6) !important;
    padding: 6px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    gap: 8px !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.25s ease !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0, 242, 254, 0.18) 0%, rgba(121, 40, 202, 0.25) 100%) !important;
    color: var(--neon-cyan) !important;
    border: 1px solid rgba(0, 242, 254, 0.4) !important;
    font-weight: 700 !important;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.2) !important;
}

/* ====== INPUTS, SELECTS, TEXTAREAS ====== */
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
    background-color: rgba(13, 20, 36, 0.8) !important;
    border: 1px solid rgba(0, 242, 254, 0.2) !important;
    color: #f1f5f9 !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
}

.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
    border-color: var(--neon-cyan) !important;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.3) !important;
}

/* ====== METRIC WIDGETS ====== */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    backdrop-filter: blur(14px) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 14px !important;
    padding: 1.1rem 1.4rem !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35) !important;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    border-color: var(--border-glass-hover) !important;
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(0, 242, 254, 0.15) !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    background: linear-gradient(135deg, #ffffff 40%, var(--neon-cyan) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ====== EXPANDERS ====== */
.streamlit-expanderHeader {
    background: rgba(15, 23, 42, 0.7) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.streamlit-expanderContent {
    background: rgba(10, 15, 26, 0.6) !important;
    border-bottom-left-radius: 10px !important;
    border-bottom-right-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
}

/* ====== CUSTOM UI COMPONENTS ====== */
.cyber-card {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(0, 242, 254, 0.18);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cyber-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00f2fe, #7928ca, transparent);
    opacity: 0.8;
}

.cyber-card:hover {
    border-color: rgba(0, 242, 254, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 242, 254, 0.15);
}

.cyber-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    font-family: 'Space Grotesk', monospace;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.badge-cyan {
    background: rgba(0, 242, 254, 0.12);
    border: 1px solid rgba(0, 242, 254, 0.4);
    color: #00f2fe;
    box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
}

.badge-purple {
    background: rgba(121, 40, 202, 0.15);
    border: 1px solid rgba(121, 40, 202, 0.4);
    color: #b388ff;
    box-shadow: 0 0 10px rgba(121, 40, 202, 0.2);
}

.badge-emerald {
    background: rgba(0, 245, 160, 0.12);
    border: 1px solid rgba(0, 245, 160, 0.4);
    color: #00f5a0;
    box-shadow: 0 0 10px rgba(0, 245, 160, 0.2);
}

.badge-rose {
    background: rgba(255, 0, 122, 0.12);
    border: 1px solid rgba(255, 0, 122, 0.4);
    color: #ff007a;
    box-shadow: 0 0 10px rgba(255, 0, 122, 0.2);
}

.pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #00f5a0;
    display: inline-block;
    box-shadow: 0 0 8px #00f5a0;
    animation: pulse 1.8s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 245, 160, 0.7); }
    70% { transform: scale(1.15); box-shadow: 0 0 0 8px rgba(0, 245, 160, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 245, 160, 0); }
}

.hero-banner-box {
    position: relative;
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 2rem;
    border: 1px solid rgba(0, 242, 254, 0.25);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
}

.hero-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 2.5rem;
    background: linear-gradient(180deg, transparent 0%, rgba(7, 9, 14, 0.95) 85%);
}

.glass-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.25rem;
    margin-top: 1rem;
}
</style>
"""

def clean_html(html_str: str) -> str:
    """Strip all leading and trailing whitespace from every line, joining as a clean HTML block."""
    if not html_str:
        return ""
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    return "\n".join(lines)

def render_html(html_str: str):
    """Directly render HTML in Streamlit guaranteed without markdown code block leakage."""
    st.markdown(clean_html(html_str), unsafe_allow_html=True)

def inject_theme():
    """Inject global CSS theme rules into current Streamlit page."""
    render_html(CYBER_CSS)

def render_page_header(title: str, subtitle: str, badge: str = "SYSTEM ACTIVE", icon: str = "⚡"):
    """Render a premium unified header banner for any module page."""
    inject_theme()
    header_html = (
        f'<div style="margin-bottom: 2rem; padding: 1.5rem 0 0.8rem 0; border-bottom: 1px solid rgba(255,255,255,0.08);">'
        f'<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">'
        f'<div>'
        f'<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">'
        f'<span style="font-size: 2rem;">{icon}</span>'
        f'<h1 style="margin: 0; font-size: 2.4rem; font-weight: 800; letter-spacing: -0.02em; background: linear-gradient(135deg, #ffffff 40%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h1>'
        f'</div>'
        f'<p style="margin: 0; color: #94a3b8; font-size: 1.05rem; font-weight: 400; max-width: 800px;">{subtitle}</p>'
        f'</div>'
        f'<div style="display: flex; align-items: center; gap: 10px;">'
        f'<div class="cyber-badge badge-cyan"><span class="pulse-dot"></span><span>{badge}</span></div>'
        f'<div class="cyber-badge badge-purple"><span>AGV COGNITION v2.5</span></div>'
        f'</div></div></div>'
    )
    render_html(header_html)

def render_cyber_card(title: str, content_html: str, badge: str = None, color: str = "cyan"):
    """Render a glassmorphic cyber-styled container card."""
    badge_html = f'<div class="cyber-badge badge-{color}">{badge}</div>' if badge else ""
    cleaned_content = clean_html(content_html)
    card_html = (
        f'<div class="cyber-card">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">'
        f'<h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #f8fafc; font-family: sans-serif;">{title}</h3>'
        f'{badge_html}'
        f'</div>'
        f'<div>{cleaned_content}</div>'
        f'</div>'
    )
    render_html(card_html)


