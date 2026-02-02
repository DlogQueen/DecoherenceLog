import streamlit as st
import time
import random
import re

def load_css(file_name="style.css"):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def render_glitch_header(text, subtext=""):
    st.markdown(f"""<div style="text-align: center; margin-bottom: 40px;">
<h1 class="glitch-text" style="font-size: 3em; margin: 0;">{text}</h1>
<p class="neon-green" style="font-size: 1.2em; letter-spacing: 2px;">{subtext}</p>
</div>""", unsafe_allow_html=True)

def render_glass_card(content):
    st.markdown(f"""<div class="glass-card">
{content}
</div>""", unsafe_allow_html=True)

def render_resonance_meter(protons, electrons, neutrals=0):
    total = protons + electrons + neutrals
    if total == 0:
        position = 50 # Center
    else:
        # Calculate balance: -100 (Pure Electron) to +100 (Pure Proton)
        balance = ((protons - electrons) / total) * 50 # Scale to +/- 50
        position = 50 + balance # Shift from center (50)
    
    # Clamp
    position = max(5, min(95, position))
    
    st.markdown(f"""<div class="meter-wrapper">
<div class="meter-scale">
<div class="scale-red"></div>
<div class="scale-grey"></div>
<div class="scale-green"></div>
</div>
<div class="meter-needle" style="left: {position}%;"></div>
</div>
<div style="display: flex; justify-content: space-between; font-size: 0.8em; color: #888; margin-top: 5px;">
<span>UNSTABLE</span>
<span>NEUTRAL</span>
<span>STABLE</span>
</div>""", unsafe_allow_html=True)

def render_nav_link(label, active=False):
    active_class = "active" if active else ""
    return f'<div class="nav-link {active_class}">{label}</div>'

def render_entanglement_alert(matched_users):
    users_str = ", ".join(matched_users)
    st.markdown(f"""<div style="
position: fixed; top: 15%; left: 5%; right: 5%; 
background: rgba(0,0,0,0.95); border: 2px solid #00FF41; 
z-index: 9999; padding: 40px; text-align: center;
box-shadow: 0 0 50px #00FF41;
animation: glitch 0.5s infinite;">
<h1 class="neon-green" style="font-size: 3em;">⚠ QUANTUM ENTANGLEMENT DETECTED ⚠</h1>
<p style="color: #FFF; font-size: 1.5em;">SYNC ESTABLISHED WITH: {users_str}</p>
<p style="color: #888;">THE FOLD IS OPENING...</p>
<p style="font-size: 0.8em; color: #555;">(Click 'ACKNOWLEDGE' below to stabilize)</p>
</div>""", unsafe_allow_html=True)

def render_terminal_boot():
    """Simulates a boot sequence with scrolling text"""
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

def get_logo_svg(size=40):
    """
    Returns the SVG code for 'The Split Atom' logo.
    Concept: An atom with a split nucleus, leaking data bits.
    """
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
<defs>
<filter id="glow">
<feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
<feMerge>
<feMergeNode in="coloredBlur"/>
<feMergeNode in="SourceGraphic"/>
</feMerge>
</filter>
</defs>
<!-- Electron Orbits -->
<ellipse cx="50" cy="50" rx="40" ry="10" stroke="#00FF41" stroke-width="1.5" fill="none" transform="rotate(45 50 50)" opacity="0.8" />
<ellipse cx="50" cy="50" rx="40" ry="10" stroke="#00FF41" stroke-width="1.5" fill="none" transform="rotate(-45 50 50)" opacity="0.8" />
<ellipse cx="50" cy="50" rx="40" ry="10" stroke="#00FF41" stroke-width="1.5" fill="none" opacity="0.5" />
<!-- The Split Nucleus -->
<path d="M 50 35 L 50 65" stroke="#000" stroke-width="4" /> <!-- Split Line -->
<!-- Left Hemisphere -->
<path d="M 46 35 A 15 15 0 0 0 46 65" fill="#00FF41" filter="url(#glow)">
<animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite" />
</path>
<!-- Right Hemisphere (Drifting/Decohering) -->
<path d="M 54 35 A 15 15 0 0 1 54 65" fill="#00FF41" filter="url(#glow)" transform="translate(2,0)">
<animateTransform attributeName="transform" type="translate" values="2,0; 4,0; 2,0" dur="0.1s" repeatCount="indefinite" />
</path>
<!-- Data Particles (Leaking) -->
<rect x="55" y="40" width="2" height="2" fill="#FFF" opacity="0.8" />
<rect x="60" y="45" width="2" height="2" fill="#FFF" opacity="0.6" />
<rect x="58" y="55" width="2" height="2" fill="#FFF" opacity="0.9" />
</svg>"""

# --- QUANTUM AI LOGIC ---

class ObserverAI:
    def __init__(self):
        # The Quantum Knowledge Base
        self.knowledge_base = {
            # Quantum Physics
            r"superposition": "In quantum mechanics, superposition is the ability of a quantum system to be in multiple states at the same time until it is measured. In this app, your posts exist in a superposition of TRUE and FALSE until the community votes.",
            r"entangle(ment)?": "Quantum entanglement is a physical phenomenon where particles remain connected so that the physical properties of one are independent of the other, even when separated by large distances. Here, 'Entanglement Alerts' notify you when someone else posts a similar anomaly.",
            r"decoherence": "Quantum decoherence is the loss of quantum coherence. In this system, it represents the breakdown of consensus reality—when too many people observe a glitch, reality stabilizes or 'decoheres'.",
            r"particle|atom": "Particles are the fundamental units of matter. We track Protons (Truth) and Electrons (Deception/Hoax) to measure the stability of a reported anomaly.",
            r"wave function": "A mathematical description of the quantum state of an isolated quantum system. It describes the probability of finding a particle in a certain state.",
            r"observer effect": "The theory that the mere observation of a phenomenon inevitably changes that phenomenon. By logging into this app, you are an Observer, and your votes change the reality rating of a post.",
            r"schrodinger": "Schrödinger's Cat is a thought experiment. A cat in a box is simultaneously alive and dead. Similarly, every unverified post here is both a Hoax and Real until you vote.",
            r"tunneling": "Quantum tunneling allows particles to pass through potential barriers. This explains how 'glitch' entities might move through solid walls.",
            
            # App Navigation / Help
            r"(how|where).*post": "To report a breach: Go to the 'HOME' tab and click the 'REPORT BREACH +' button at the top right.",
            r"(how|where).*vote": "You can vote on any post in the FEED. Click 'Real (+)' to add a Proton or 'Fake (-)' to add an Electron.",
            r"what.*(proton|electron)": "PROTONS (+) indicate you believe the evidence is authentic. ELECTRONS (-) indicate you believe it is a hoax or system error.",
            r"resonance meter": "The Resonance Meter visualizes the community consensus. Left (Red) means Unstable/Hoax. Right (Green) means Stable/Truth. Center is Neutral.",
            r"profile|avatar": "Go to the 'PROFILE' tab to view your stats, edit your bio, or update your avatar.",
            r"archive|categories": "The Archives are located at the top of the Home Feed. Click on icons like UFO, Cryptid, or Time to filter specific anomalies.",
            r"friend|connect": "Go to the 'OBSERVERS' tab to see connection requests or chat with other agents.",
            
            # General Chat
            r"hello|hi|hey": "Greetings, Observer. I am connected to the Quantum Field. How may I assist your navigation?",
            r"who are you": "I am The Observer. An AI construct designed to monitor decoherence events and guide agents like yourself through the Fold.",
            r"help": "I can explain quantum concepts (try 'What is superposition?') or help you navigate (try 'How do I post?').",
            r"thank": "You are welcome. Keep watching the static.",
            r"real|truth": "Truth is a variable. We merely aggregate the data points."
        }
        
        self.fallback_responses = [
            "I am analyzing the quantum foam for that query... The signal is ambiguous.",
            "My databanks are searching the multiverse... Please rephrase your query.",
            "That concept is currently encrypted in a higher dimension.",
            "I detect a query, but the wave function has collapsed. Try asking about 'superposition' or 'how to post'.",
            "Accessing the Akashic Records... Data corrupted. Please ask about app functions or quantum theory."
        ]

    def get_response(self, user_msg):
        """
        Intelligent response generation using regex matching against the knowledge base.
        Simulates 'Internet' connection delay.
        """
        msg = user_msg.lower()
        
        # Simulate processing delay (Thinking)
        time.sleep(0.5) 
        
        # Check Knowledge Base
        for pattern, response in self.knowledge_base.items():
            if re.search(pattern, msg):
                return f"🔍 **ANALYSIS:** {response}"
        
        # Check for calculation requests (simple math as a 'smart' feature)
        if re.search(r"calculate|math", msg):
            return "🧮 I can process quantum probability, but simple arithmetic is trivial. I focus on the physics of reality."

        # Fallback
        return f"📡 **SIGNAL WEAK:** {random.choice(self.fallback_responses)}"

# Singleton Instance
observer_ai = ObserverAI()
