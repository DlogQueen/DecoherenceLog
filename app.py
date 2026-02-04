import streamlit as st
import time
import random
import os
from utils import load_css, render_glitch_header, render_glass_card, render_resonance_meter, render_entanglement_alert, render_terminal_boot, get_logo_html, render_atoms, observer_ai
import auth
import database

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="DECOHERENCE LOG",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
database.init_db()

load_css()

# --- STATE MANAGEMENT ---
if 'initialized' not in st.session_state:
    st.session_state['initialized'] = False

if 'page' not in st.session_state:
    st.session_state['page'] = 'feed'

if 'user' not in st.session_state:
    st.session_state['user'] = {}

if 'entanglement_alert' not in st.session_state:
    st.session_state['entanglement_alert'] = None

if 'notifications' not in st.session_state:
    st.session_state['notifications'] = []

if 'notification_settings' not in st.session_state:
    st.session_state['notification_settings'] = {
        "entanglements": True,
        "messages": True,
        "brand": True,
        "observers": True
    }

# --- ALGORITHMS ---

def add_notification(n_type, message):
    settings = st.session_state['notification_settings']
    if settings.get(n_type, True):
        new_notif = {
            "id": int(time.time() * 1000),
            "type": n_type,
            "message": message,
            "time": time.strftime("%H:%M"),
            "read": False
        }
        st.session_state['notifications'].insert(0, new_notif)
        st.toast(f"[{n_type.upper()}] {message}", icon="⚠️")

# --- VIEWS ---

def sidebar_nav():
    with st.sidebar:
        # Logo and Subheader
        st.image("assets/logo.png", width=120)
        st.markdown("""
        <div style="margin-bottom: 20px; font-size: 0.8em; color: #00f2ff; letter-spacing: 1px; font-family: 'Share Tech Mono', monospace;">
        TRACKING THE GLITCHES<br>IN OUR REALITY
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📡 NEURAL LINK")
        if st.button("THE GLOBAL FEED", use_container_width=True):
            st.session_state['page'] = 'feed'
            st.rerun()
        if st.button("👤 MY ARCHIVE", use_container_width=True):
            st.session_state['page'] = 'profile'
            st.rerun()
        if st.button("🌀 THE FOLD", use_container_width=True):
            st.session_state['page'] = 'fold'
            st.rerun()
            
        st.markdown("---")
        
        if auth.is_admin():
            if st.button("🛠️ ARCHITECT", use_container_width=True):
                st.session_state['page'] = 'admin'
                st.rerun()
        
        if st.button("❌ SEVER LINK (LOGOUT)", use_container_width=True):
            auth.logout_user()
            st.rerun()

def app_bar():
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.markdown(f"""<div style="display: flex; align-items: center;">
        {get_logo_html(50)}
        <div style="line-height: 1.1; margin-left: 10px;">
            <div style="font-weight: bold; color: #00f2ff; font-size: 1.2em;">THE DECOHERENCE LOG</div>
            <div style="font-size: 0.6em; color: #aaa; letter-spacing: 1px;">SANCTUARY MODE ACTIVE</div>
        </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        query = st.text_input("SEARCH FREQUENCY...", label_visibility="collapsed", placeholder="Search reality...")
        if query:
            st.toast(f"SEARCHING: {query}...")
    with c3:
        if st.button("💬", key="msg_icon"):
            st.session_state['page'] = 'fold'
            st.rerun()
    st.markdown("---")

def feed_view():
    app_bar()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h2 class="neon-cyan">GLOBAL ECHO CHAMBER</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("LOG NEW BREACH +", type="primary"):
            st.session_state['page'] = 'post'
            st.rerun()

    posts = database.get_all_posts()
    
    for post in posts:
        with st.container():
            # Post Card
            content = f"""
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="display: flex; align-items: center;">
                    <div style="width: 40px; height: 40px; background: #111; border: 1px solid #00f2ff; border-radius: 50%; margin-right: 10px;"></div>
                    <div>
                        <span class="neon-cyan" style="font-weight: bold;">@{post['username']}</span><br>
                        <span style="color: #666; font-size: 0.8em;">{post['created_at']}</span>
                    </div>
                </div>
                <div style="border: 1px solid rgba(0, 242, 255, 0.3); padding: 2px 8px; font-size: 0.7em; color: #00f2ff; border-radius: 4px;">VERIFIED OBSERVER</div>
            </div>
            <hr style="border-color: rgba(0, 242, 255, 0.3); opacity: 0.5;">
            <p style="font-size: 1.1em; color: #fff; margin-top: 10px;">{post['status_text']}</p>
            """
            
            # Media
            if post['media_path']:
                if post['media_type'] == 'video':
                    st.video(post['media_path'])
                else:
                    st.image(post['media_path'])
            
            content += f'<div style="font-size: 0.8em; color: #008f99; margin-top: 10px;">RESONANCE: {", ".join(post["tags"].split(","))}</div>'
            render_glass_card(content)
            
            # Interaction
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                if st.button(f"👁️ ACKNOWLEDGE ({post['protons']})", key=f"ack_{post['id']}"):
                    # Treat protons as "Acknowledge" count
                    database.add_vote(auth.get_current_user()['id'], post['id'], "proton")
                    st.toast("GLITCH VALIDATED.")
                    st.rerun()
            with c2:
                if st.button("🚩 REPORT", key=f"rep_{post['id']}"):
                    st.toast("REPORT FILED TO ARCHITECT.")
            
    sidebar_nav()

def post_view():
    st.markdown('<h2 class="neon-cyan">LOG NEW BREACH</h2>', unsafe_allow_html=True)
    with st.form("breach_form"):
        status = st.text_area("STATUS REPORT", placeholder="Describe the anomaly...")
        tags = st.text_input("RESONANCE TAGS", placeholder="time, glitch, shadow")
        media = st.file_uploader("UPLOAD EVIDENCE", type=['jpg', 'png', 'mp4'])
        submitted = st.form_submit_button("TRANSMIT TO FEED")
        
        if submitted and status:
            user = auth.get_current_user()
            media_path = ""
            media_type = "image"
            if media:
                if not os.path.exists("uploads"):
                    os.makedirs("uploads")
                media_path = os.path.join("uploads", media.name)
                with open(media_path, "wb") as f:
                    f.write(media.getbuffer())
                if media.type.startswith("video"):
                    media_type = "video"
            
            post_id = database.create_post(user['id'], user['username'], status, media_path, media_type, tags)
            matches = database.check_for_entanglements(post_id, tags)
            if matches:
                st.session_state['entanglement_alert'] = matches
            
            st.success("BREACH LOGGED.")
            time.sleep(1)
            st.session_state['page'] = 'feed'
            st.rerun()
    sidebar_nav()

def profile_view():
    app_bar()
    st.markdown('<h2 class="neon-cyan">ARCHIVE (PROFILE)</h2>', unsafe_allow_html=True)
    user = auth.get_current_user() # Get from Auth/DB
    # If user dict is empty in auth, fall back
    if not user:
        st.error("Profile Error")
        return

    c1, c2 = st.columns([1, 3])
    with c1:
        st.image("https://via.placeholder.com/150/00f2ff/000000?text=AGENT", width=150)
    with c2:
        st.title(user.get('username', 'Agent'))
        st.markdown(f"**Role:** {user.get('role', 'Observer')}")
        st.markdown(f"**Status:** CONNECTED")

    st.markdown("### LOGGED BREACHES")
    posts = database.get_all_posts()
    my_posts = [p for p in posts if p['username'] == user.get('username')]
    
    if not my_posts:
        st.info("No breaches logged yet.")
    else:
        for post in my_posts:
            render_glass_card(f"""
            <div style="margin-bottom: 5px; color: #888;">{post['created_at']}</div>
            <p>{post['status_text']}</p>
            <div style="color: #00f2ff;">Acknowledgments: {post['protons']}</div>
            """)
    sidebar_nav()

def fold_view():
    st.markdown('<h2 class="neon-cyan">THE FOLD (AI OBSERVER)</h2>', unsafe_allow_html=True)
    render_glass_card("""
    <h3 style="margin:0; color: #fff;">THE OBSERVER AI</h3>
    <p style="font-size: 0.8em; color: #008f99;">STATUS: CONNECTED TO QUANTUM FIELD</p>
    """)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Query the Quantum Field..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        response = observer_ai.get_response(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    sidebar_nav()

def admin_view():
    app_bar()
    st.markdown('<h2 class="warning-red">ARCHITECT DASHBOARD</h2>', unsafe_allow_html=True)
    if st.button("← EXIT GOD MODE"):
        st.session_state['page'] = 'feed'
        st.rerun()
        
    reported = database.get_reported_posts()
    if not reported:
        st.info("SYSTEM STABLE. NO ANOMALIES REPORTED.")
    else:
        for post in reported:
            st.error(f"REPORTED POST #{post['id']} by {post['username']}")
            st.write(post['status_text'])
            if st.button("EXTERMINATE", key=f"del_{post['id']}", type="primary"):
                database.update_post_status(post['id'], "deleted")
                st.rerun()
    sidebar_nav()

def void_layer_view():
    utils.render_void_intro()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("INITIALIZE SYSTEM_", use_container_width=True):
            with st.spinner("DECRYPTING REALITY..."):
                time.sleep(1.5)
                st.session_state['initialized'] = True
                st.rerun()

def login_view():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        render_glass_card("""<h2 class="neon-cyan" style="text-align: center;">SECURITY CLEARANCE</h2>
        <p style="text-align: center; color: #888;">BIOMETRIC VERIFICATION REQUIRED</p>
        <hr style="border-color: #333;">""")
        
        with st.form("login_form"):
            username = st.text_input("CODENAME", placeholder="Enter Agent ID")
            password = st.text_input("PASSPHRASE", type="password")
            remember = st.checkbox("MAINTAIN QUANTUM LINK")
            
            if st.form_submit_button("AUTHENTICATE"):
                if auth.verify_login(username.lower(), password):
                    auth.login_user(username, remember_me=remember)
                    st.success("ACCESS GRANTED.")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("ACCESS DENIED.")
        st.markdown("<div style='text-align: center; font-size: 0.8em; color: #444;'>Default: agent_smith / TheMatrixHasYou_2024</div>", unsafe_allow_html=True)

# --- MAIN CONTROLLER ---

if not st.session_state['initialized']:
    void_layer_view()
else:
    if not auth.check_auth():
        login_view()
    else:
        if st.session_state['entanglement_alert']:
            render_entanglement_alert(st.session_state['entanglement_alert'])
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                if st.button("ACKNOWLEDGE SYNC", key="ack_alert_main"):
                    st.session_state['entanglement_alert'] = None
                    st.rerun()
        
        # Router
        page = st.session_state['page']
        if page == 'feed': feed_view()
        elif page == 'post': post_view()
        elif page == 'profile': profile_view()
        elif page == 'fold': fold_view()
        elif page == 'admin': admin_view()
        else: feed_view()
