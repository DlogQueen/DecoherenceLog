import streamlit as st
import time
import os
import database
import auth
import utils

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="DECOHERENCE LOG",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Database
database.init_db()

# Load Cyberpunk Styles
utils.load_css()

# --- SESSION STATE INITIALIZATION ---
if 'initialized' not in st.session_state:
    st.session_state['initialized'] = False

if 'page' not in st.session_state:
    st.session_state['page'] = 'feed'

if 'entanglement_alert' not in st.session_state:
    st.session_state['entanglement_alert'] = None

# --- VIEWS ---

def void_layer():
    """The Pre-Init Warning Screen"""
    utils.render_void_intro()
    # Center the button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
        if st.button("INITIALIZE SYSTEM_", use_container_width=True):
            with st.spinner("DECRYPTING REALITY..."):
                time.sleep(2)
                st.session_state['initialized'] = True
                st.rerun()

def login_layer():
    """The Security Clearance Screen"""
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h2 class="neon-green">SECURITY CLEARANCE REQUESTED</h2>
            <p style="color: #888;">BIOMETRIC VERIFICATION REQUIRED</p>
            <hr style="border-color: #333;">
            <p style="font-size: 0.8em; color: #555;">
            Identity required for World Line 0.00%...<br>
            Status: System Breach in Progress
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Google Auth Button
        if auth.google_login_btn():
            # Mock successful login for prototype
            auth.login_user("Agent_Ryleigh", "ryleigh@decoherence.log")
            st.success("BIOMETRICS CONFIRMED.")
            time.sleep(1)
            st.rerun()

def sidebar_nav():
    """The Neural Link Sidebar"""
    with st.sidebar:
        st.markdown("### 📡 NEURAL LINK")
        
        if st.button("THE GLOBAL FEED", use_container_width=True):
            st.session_state['page'] = 'feed'
            st.rerun()
            
        if st.button("👤 MY ARCHIVE", use_container_width=True):
            st.session_state['page'] = 'archive'
            st.rerun()
            
        if st.button("🌀 THE FOLD", use_container_width=True):
            st.session_state['page'] = 'fold'
            st.rerun()
            
        st.markdown("---")
        
        if auth.is_admin():
            if st.button("🛠️ ARCHITECT", use_container_width=True):
                st.session_state['page'] = 'architect'
                st.rerun()
        
        if st.button("❌ SEVER LINK (LOGOUT)", use_container_width=True):
            auth.logout_user()
            st.rerun()

def feed_view():
    st.markdown('<h1 class="neon-green glitch-text">GLOBAL SUPERPOSITION FEED</h1>', unsafe_allow_html=True)
    
    # Post Button
    if st.button("LOG NEW BREACH +"):
        st.session_state['page'] = 'post'
        st.rerun()
    
    # Get Posts
    posts = database.get_all_posts()
    
    for post in posts:
        with st.container():
            # Card Container
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between;">
                    <span class="neon-green">@{post['username']}</span>
                    <span style="color: #666;">{post['created_at']}</span>
                </div>
                <hr style="border-color: #00FF41; opacity: 0.3;">
                <p style="font-size: 1.2em;">{post['status_text']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Media (if exists)
            if post['media_path']:
                if post['media_type'] == 'video':
                    st.video(post['media_path'])
                else:
                    st.image(post['media_path'])
            
            # Resonance Meter & Atoms
            c1, c2 = st.columns([2, 1])
            with c1:
                utils.render_resonance_meter(post['protons'], post['electrons'], post['neutrons'])
            with c2:
                # Share Button
                st.markdown(f"""
                <div style="text-align: right;">
                    <a href="#" style="color: #00FF41; text-decoration: none; border: 1px solid #00FF41; padding: 5px;">
                        🔗 OUTSOURCE
                    </a>
                </div>
                """, unsafe_allow_html=True)

            # Voting Atoms
            vote = utils.render_atoms(post['id'])
            if vote:
                user = auth.get_current_user()
                if database.add_vote(user['id'], post['id'], vote):
                    st.toast(f"PARTICLE INJECTED: {vote.upper()}")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.toast("ENERGY SIGNATURE ALREADY RECORDED.")

def post_view():
    st.markdown('<h2 class="neon-green">LOG NEW BREACH</h2>', unsafe_allow_html=True)
    
    with st.form("breach_form"):
        status = st.text_area("STATUS REPORT", placeholder="Describe the anomaly...")
        tags = st.text_input("RESONANCE TAGS", placeholder="time, glitch, shadow")
        media = st.file_uploader("UPLOAD EVIDENCE", type=['jpg', 'png', 'mp4'])
        
        submitted = st.form_submit_button("TRANSMIT TO FEED")
        
        if submitted and status:
            user = auth.get_current_user()
            media_path = ""
            media_type = "image"
            
            # Handle Upload
            if media:
                # Create uploads dir if not exists
                if not os.path.exists("uploads"):
                    os.makedirs("uploads")
                
                media_path = os.path.join("uploads", media.name)
                with open(media_path, "wb") as f:
                    f.write(media.getbuffer())
                
                if media.type.startswith("video"):
                    media_type = "video"
            
            # Create Post
            post_id = database.create_post(user['id'], user['username'], status, media_path, media_type, tags)
            
            # Check Entanglement
            matches = database.check_for_entanglements(post_id, tags)
            if matches:
                st.session_state['entanglement_alert'] = matches
            
            st.success("BREACH LOGGED.")
            time.sleep(1)
            st.session_state['page'] = 'feed'
            st.rerun()

def architect_view():
    st.markdown('<h2 class="warning-red">ARCHITECT DASHBOARD</h2>', unsafe_allow_html=True)
    st.warning("⚠ ROOT ACCESS GRANTED ⚠")
    
    reported = database.get_reported_posts()
    if not reported:
        st.info("SYSTEM STABLE. NO ANOMALIES REPORTED.")
    else:
        for post in reported:
            st.error(f"REPORTED POST #{post['id']} by {post['username']}")
            st.write(post['status_text'])
            c1, c2 = st.columns(2)
            with c1:
                if st.button("EXTERMINATE", key=f"del_{post['id']}", type="primary"):
                    database.update_post_status(post['id'], "deleted")
                    st.rerun()
            with c2:
                if st.button("AUTHORIZE", key=f"auth_{post['id']}"):
                    database.update_post_status(post['id'], "active")
                    st.rerun()

def archive_view():
    user = auth.get_current_user()
    st.markdown(f'<h2 class="neon-green">ARCHIVE: {user["username"]}</h2>', unsafe_allow_html=True)
    # Simple list of user's posts could go here
    st.info("ACCESSING PERSONAL LOGS...")

def fold_view():
    st.markdown('<h2 class="neon-green">THE FOLD</h2>', unsafe_allow_html=True)
    st.info("SEARCHING FOR ENTANGLED FREQUENCIES...")
    # Chat UI would go here

# --- MAIN CONTROLLER ---

# 1. Void Layer
if not st.session_state['initialized']:
    void_layer()

# 2. Auth Layer
elif not auth.check_password():
    login_layer()

# 3. Main System
else:
    # Global Alert Check
    if st.session_state['entanglement_alert']:
        utils.render_entanglement_alert(st.session_state['entanglement_alert'])
        if st.button("ACKNOWLEDGE SYNC", key="ack_main"):
            st.session_state['entanglement_alert'] = None
            st.rerun()
            
    sidebar_nav()
    
    if st.session_state['page'] == 'feed':
        feed_view()
    elif st.session_state['page'] == 'post':
        post_view()
    elif st.session_state['page'] == 'architect':
        architect_view()
    elif st.session_state['page'] == 'archive':
        archive_view()
    elif st.session_state['page'] == 'fold':
        fold_view()
