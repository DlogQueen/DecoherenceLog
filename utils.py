import streamlit as st
import base64
import os

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_void_intro():
    """Renders the boot sequence."""
    st.markdown("""
    <div class="void-warning">
        <div class="void-text">
            ⚠️ REALITY DECOHERENCE DETECTED ⚠️<br>
            <span style="font-size: 0.5em; color: #00FF41;">PROCEED AT YOUR OWN RISK</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_resonance_meter(protons, electrons, neutrals=0):
    """
    Renders an analog-style gauge based on the ratio.
    """
    total = protons + electrons + neutrals
    if total == 0:
        ratio = 50 # Neutral
    else:
        # Calculate percentage towards Proton (100) or Electron (0)
        # We start at 50. Protons add, Electrons subtract.
        # Simple algorithm: P / (P + E) * 100
        denom = protons + electrons
        if denom == 0:
            ratio = 50
        else:
            ratio = (protons / denom) * 100
            
    # Color logic
    color = "#888" # Neutral
    if ratio > 60: color = "#00FF41" # Green/Real
    if ratio < 40: color = "#FF003C" # Red/Fake
    
    # HTML for the Gauge
    st.markdown(f"""
    <div class="resonance-container">
        <div style="font-size: 0.8em; color: #888;">STABILITY</div>
        <div style="
            width: 100%; 
            height: 10px; 
            background: #222; 
            margin: 0 10px; 
            border-radius: 5px;
            position: relative;
            border: 1px solid #444;
        ">
            <div style="
                position: absolute;
                left: {ratio}%;
                top: -5px;
                width: 4px;
                height: 20px;
                background: {color};
                box-shadow: 0 0 10px {color};
                transition: left 0.5s ease;
            "></div>
        </div>
        <div style="font-size: 0.8em; color: {color};">{int(ratio)}%</div>
    </div>
    """, unsafe_allow_html=True)

def render_entanglement_alert(matches):
    """
    Full screen alert for entanglement.
    """
    st.markdown(f"""
    <div style="
        position: fixed; 
        top: 0; left: 0; width: 100%; height: 100%; 
        background: rgba(0,0,0,0.9); 
        z-index: 10000; 
        display: flex; 
        flex-direction: column;
        align-items: center; 
        justify-content: center;
        animation: flicker 0.2s infinite;
    ">
        <h1 class="neon-green" style="font-size: 4em; text-align: center;">! SYSTEM SYNC DETECTED !</h1>
        <h2 style="color: #FFF;">MULTIPLE WITNESSES FOUND</h2>
        <div style="border: 1px solid #00FF41; padding: 20px; margin-top: 20px;">
            <p>MATCH COUNT: {len(matches)}</p>
            <p>OPENING THE FOLD...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_atoms(post_id):
    """
    Renders the 3 interaction atoms.
    Since Streamlit buttons are limited in styling, we use columns and emojis/labels 
    that match the CSS classes we defined.
    """
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⚛️ PROTON (+)", key=f"proton_{post_id}", use_container_width=True):
            return "proton"
    with c2:
        if st.button("⚡ ELECTRON (-)", key=f"electron_{post_id}", use_container_width=True):
            return "electron"
    with c3:
        if st.button("⚪ NEUTRON (0)", key=f"neutron_{post_id}", use_container_width=True):
            return "neutron"
    return None

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
