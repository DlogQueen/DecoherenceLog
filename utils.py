import streamlit as st
import time
import random
import re
import socket
import base64
import os

@st.cache_data
def get_img_as_base64(file_path):
    """Reads an image file and converts it to base64 string."""
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_local_ip():
    """Gets the local network IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def load_css(file_name="style.css"):
    with open(file_name) as f:
        css = f.read()
    
    # Inject Background
    bg_b64 = get_img_as_base64("assets/background.png")
    if bg_b64:
        css += f"""
        .stApp {{
            background-image: url("data:image/png;base64,{bg_b64}");
            background-attachment: fixed;
            background-size: cover;
        }}
        """
        # Add overlay via pseudo-element to ensure readability
        css += """
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(5, 5, 5, 0.8);
            z-index: -1;
            pointer-events: none;
        }
        """
        
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def render_void_intro():
    """Renders the boot sequence."""
    st.markdown("""
    <div class="void-warning">
        <div class="void-text">
            ⚠️ REALITY DECOHERENCE DETECTED ⚠️<br>
            <span style="font-size: 0.5em; color: #00f2ff;">PROCEED AT YOUR OWN RISK</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_glitch_header(text, subtext=""):
    st.markdown(f"""<div style="text-align: center; margin-bottom: 40px;">
<h1 class="glitch-text" style="font-size: 3em; margin: 0;">{text}</h1>
<p class="neon-cyan" style="font-size: 1.2em; letter-spacing: 2px;">{subtext}</p>
</div>""", unsafe_allow_html=True)

def render_glass_card(content):
    st.markdown(f"""<div class="glass-card">
{content}
</div>""", unsafe_allow_html=True)

def render_resonance_meter(protons, electrons, neutrals=0):
    total = protons + electrons + neutrals
    if total == 0:
        position = 50 # Center
        ratio = 50
    else:
        balance = ((protons - electrons) / total) * 50 
        position = 50 + balance 
        denom = protons + electrons
        if denom == 0:
            ratio = 50
        else:
            ratio = (protons / denom) * 100
    
    position = max(5, min(95, position))
    
    color = "#888" 
    if ratio > 60: color = "#00f2ff" # Cyan/Real
    if ratio < 40: color = "#ff0000" # Red/Fake
    
    st.markdown(f"""<div class="meter-wrapper">
<div class="meter-scale">
<div class="scale-red"></div>
<div class="scale-grey"></div>
<div class="scale-cyan"></div>
</div>
<div class="meter-needle" style="left: {position}%;"></div>
</div>
<div style="display: flex; justify-content: space-between; font-size: 0.8em; color: #888; margin-top: 5px;">
<span>UNSTABLE</span>
<span>NEUTRAL</span>
<span>STABLE</span>
</div>""", unsafe_allow_html=True)

def render_entanglement_alert(matched_users):
    if isinstance(matched_users, list):
        users_str = ", ".join(str(u) for u in matched_users)
    else:
        users_str = "UNKNOWN ENTITY"
        
    st.markdown(f"""<div style="
position: fixed; top: 15%; left: 5%; right: 5%; 
background: rgba(0,0,0,0.95); border: 2px solid #ff0000; 
z-index: 9999; padding: 40px; text-align: center;
box-shadow: 0 0 50px #ff0000;
animation: glitch 0.5s infinite;">
<h1 class="warning-red" style="font-size: 3em;">⚠ QUANTUM ENTANGLEMENT DETECTED ⚠</h1>
<p style="color: #FFF; font-size: 1.5em;">SYNC ESTABLISHED WITH: {users_str}</p>
<p style="color: #888;">THE FOLD IS OPENING...</p>
<p style="font-size: 0.8em; color: #555;">(Click 'ACKNOWLEDGE' below to stabilize)</p>
</div>""", unsafe_allow_html=True)

def render_terminal_boot():
    lines = [
        "INITIALIZING KERNEL...",
        "LOADING REALITY DRIVERS...",
        "BYPASSING SECURITY PROTOCOLS...",
        "CONNECTING TO WORLD LINE 0.00%...",
        "SYNCING WITH QUANTUM SERVER...",
        "DECRYPTING USER DATA...",
        "SYSTEM INTEGRITY: 48%... 72%... 99%...",
        "BREACH DETECTED.",
        "WELCOME TO THE DECOHERENCE LOG."
    ]
    placeholder = st.empty()
    text_buffer = ""
    for line in lines:
        text_buffer += f"> {line}<br>"
        placeholder.markdown(f"""<div class="terminal-text">
{text_buffer}
<span class="cursor"></span>
</div>""", unsafe_allow_html=True)
        time.sleep(0.3)
    return placeholder

def get_logo_html(size=40):
    """Returns the IMG tag for the logo with glow effect."""
    logo_b64 = get_img_as_base64("assets/logo.png")
    if logo_b64:
        return f'<img src="data:image/png;base64,{logo_b64}" width="{size}" style="filter: drop-shadow(0 0 5px #00f2ff);">'
    return ""

def render_atoms(post_id):
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👁️ ACKNOWLEDGE", key=f"ack_{post_id}", use_container_width=True):
            return "acknowledge"
    with c2:
        if st.button("🚩 REPORT GLITCH", key=f"report_{post_id}", use_container_width=True):
            return "report"
    return None

# --- QUANTUM AI LOGIC ---

class ObserverAI:
    def __init__(self):
        self.knowledge_base = {
            r"superposition": "In quantum mechanics, superposition is the ability of a quantum system to be in multiple states at the same time until it is measured.",
            r"entangle(ment)?": "Quantum entanglement is a physical phenomenon where particles remain connected so that the physical properties of one are independent of the other.",
            r"decoherence": "Quantum decoherence is the loss of quantum coherence. In this system, it represents the breakdown of consensus reality.",
            r"(how|where).*post": "To report a breach: Go to the 'HOME' tab and click the 'LOG NEW BREACH +' button.",
            r"hello|hi|hey": "Greetings, Observer. I am connected to the Quantum Field. How may I assist your navigation?",
            r"who are you": "I am The Observer. An AI construct designed to monitor decoherence events and guide agents like yourself through the Fold.",
            r"help": "I can explain quantum concepts or help you navigate.",
            r"safe|report": "This is a Sanctuary. Use the 'REPORT GLITCH' button to flag any entity violating our peace."
        }
        
        self.fallback_responses = [
            "I am searching the local archives... No matching data found.",
            "My quantum sensors are active, but that query is outside my current parameters.",
            "I am a local construct. Please ask about 'superposition', 'entanglement', or 'how to use the app'.",
            "The Fold is vast. I can only guide you on Physics and App Navigation."
        ]

    def get_response(self, user_msg):
        msg = user_msg.lower()
        time.sleep(0.3) 
        for pattern, response in self.knowledge_base.items():
            if re.search(pattern, msg):
                return f"🔍 **ANALYSIS:** {response}"
        return f"🤖 **SYSTEM:** {random.choice(self.fallback_responses)}"

observer_ai = ObserverAI()
