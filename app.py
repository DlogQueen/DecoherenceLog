import streamlit as st
import time
import random
from utils import load_css, render_glitch_header, render_glass_card, render_resonance_meter, render_entanglement_alert, render_terminal_boot, get_logo_svg, observer_ai
import auth

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="DECOHERENCE LOG",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_css()

# --- STATE MANAGEMENT ---
if 'initialized' not in st.session_state:
    st.session_state['initialized'] = False

if 'page' not in st.session_state:
    st.session_state['page'] = 'feed'

if 'user' not in st.session_state:
    st.session_state['user'] = {}

if 'posts' not in st.session_state:
    st.session_state['posts'] = [
        {
            "id": 101,
            "user": "Chronos_Walker",
            "time": "14:02",
            "status": "The clock tower struck 13. I have audio proof.",
            "tags": ["time", "clock", "audio"],
            "protons": 45,
            "electrons": 5,
            "neutrals": 2,
            "comments": []
        },
        {
            "id": 102,
            "user": "Glitch_Hunter",
            "time": "13:55",
            "status": "Shadow person seen in the hallway. It didn't cast a reflection.",
            "tags": ["shadow", "hallway", "visual"],
            "protons": 12,
            "electrons": 30,
            "neutrals": 5,
            "comments": []
        }
    ]

if 'categories' not in st.session_state:
    st.session_state['categories'] = [
        {"title": "DIMENSIONAL GLITCHES", "desc": "Multiverse, Time Slips", "icon": "⏳"},
        {"title": "AERIAL ANOMALIES", "desc": "UFO / UAP", "icon": "🛸"},
        {"title": "PARANORMAL EVENTS", "desc": "Hauntings / Psychic", "icon": "👻"},
        {"title": "CRYPTID SIGHTINGS", "desc": "Bigfoot / Nessie", "icon": "👣"},
        {"title": "EARTH MYSTERIES", "desc": "The Hum / Ley Lines", "icon": "🌍"},
        {"title": "CONSPIRACY THEORIES", "desc": "Theories & Debates", "icon": "👁️"}
    ]

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'entanglement_alert' not in st.session_state:
    st.session_state['entanglement_alert'] = None

if 'notifications' not in st.session_state:
    st.session_state['notifications'] = [
        {"id": 1, "type": "brand", "message": "SYSTEM UPDATE: Version 2.0.4 loaded. Reality filters stabilized.", "time": "Now", "read": False}
    ]

if 'notification_settings' not in st.session_state:
    st.session_state['notification_settings'] = {
        "entanglements": True,
        "messages": True,
        "brand": True,
        "observers": True
    }

# --- ALGORITHMS ---

def get_ai_response(user_msg):
    """
    Simulates the AI Observer response using the upgraded Knowledge Base.
    """
    return observer_ai.get_response(user_msg)

def add_notification(n_type, message):
    """
    Adds a notification if the user has enabled that category.
    types: 'entanglements', 'messages', 'brand', 'observers'
    """
    settings = st.session_state['notification_settings']
    # Map distinct event types to setting keys
    setting_key = n_type
    
    if settings.get(setting_key, True):
        new_notif = {
            "id": int(time.time() * 1000),
            "type": n_type,
            "message": message,
            "time": time.strftime("%H:%M"),
            "read": False
        }
        st.session_state['notifications'].insert(0, new_notif)
        # Real-time Toast
        st.toast(f"[{n_type.upper()}] {message}", icon="⚠️")

def check_entanglement(new_status, new_tags):
    """
    Scans existing posts for similarities.
    """
    matches = []
    new_words = set(new_status.lower().split())
    new_tags_set = set(new_tags)
    
    for post in st.session_state['posts']:
        # Don't match with self (though user isn't in list yet technically)
        post_words = set(post['status'].lower().split())
        post_tags = set(post['tags'])
        
        # Intersection
        word_overlap = new_words.intersection(post_words)
        tag_overlap = new_tags_set.intersection(post_tags)
        
        if len(word_overlap) > 2 or len(tag_overlap) > 0:
            matches.append(post['user'])
            
    return matches

# --- VIEWS ---

def void_layer_view():
    """The Pre-Init Warning Screen with Boot Sequence"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if 'boot_complete' not in st.session_state:
        st.session_state['boot_complete'] = False

    if not st.session_state['boot_complete']:
        placeholder = render_terminal_boot()
        time.sleep(1)
        st.session_state['boot_complete'] = True
        placeholder.empty()

    render_glitch_header("THE DECOHERENCE LOG", "TRACKING THE GLITCHES IN OUR REALITY")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""<div style="border: 1px solid #333; padding: 20px; background: #050505; color: #888; font-family: monospace; margin-bottom: 30px; text-align: center;">
> WARNING: UNAUTHORIZED ACCESS ATTEMPT<br>
> REALITY SYNC: UNSTABLE<br>
> PROCEED AT YOUR OWN RISK
</div>""", unsafe_allow_html=True)
        
        # App Explanation
        st.markdown("""<div style="text-align: center; margin-bottom: 30px; color: #00FF41; font-family: 'Share Tech Mono', monospace;">
<p style="font-size: 1.1em; text-transform: uppercase; letter-spacing: 1px;">
THE DECOHERENCE LOG IS A SOCIAL MEDIA ARCHIVE FOR RAW EVIDENCE OF ANOMALIES THAT SHOULD NOT EXIST.
</p>
<p style="font-size: 0.9em; color: #aaa;">
USERS VOTE TO DETERMINE REALITY: <br>
<span style="color: #00FF41;">PROTON (+)</span> = BELIEVE | <span style="color: #FF003C;">ELECTRON (-)</span> = HOAX
</p>
</div>""", unsafe_allow_html=True)
        
        # Center the button
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("INITIALIZE SYSTEM_"):
                with st.spinner("DECRYPTING REALITY..."):
                    time.sleep(1.5)
                    st.session_state['initialized'] = True
                    st.rerun()

def login_view():
    """Security Clearance"""
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        render_glass_card("""<h2 class="neon-green" style="text-align: center;">SECURITY CLEARANCE</h2>
<p style="text-align: center; color: #888;">BIOMETRIC VERIFICATION REQUIRED</p>
<hr style="border-color: #333;">
<p style="font-size: 0.8em; color: #555;">
By proceeding, you acknowledge that observed reality is subject to change based on quantum consensus.
</p>""")
        
        with st.form("login_form"):
            username = st.text_input("CODENAME", placeholder="Enter Agent ID")
            password = st.text_input("PASSPHRASE", type="password", placeholder="******")
            remember = st.checkbox("MAINTAIN QUANTUM LINK (STAY LOGGED IN)")
            
            if st.form_submit_button("AUTHENTICATE"):
                with st.spinner("HANDSHAKING WITH GATEKEEPER..."):
                    time.sleep(1.0)
                    if auth.verify_login(username.lower(), password):
                        auth.login_user(username, remember_me=remember)
                        st.success("ACCESS GRANTED.")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED. INCORRECT CREDENTIALS.")
                        
        st.markdown("<div style='text-align: center; font-size: 0.8em; color: #444;'>Default Access: agent_smith / matrix</div>", unsafe_allow_html=True) 

def app_bar():
    """Top App Bar: Logo, Search, Messenger"""
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        # Use the SVG logo instead of just text
        st.markdown(f"""<div style="display: flex; align-items: center;">
{get_logo_svg(50)}
<div style="line-height: 1.1; margin-left: 10px;">
    <div style="font-weight: bold; color: #00FF41; font-size: 1.2em;">THE DECOHERENCE LOG</div>
    <div style="font-size: 0.6em; color: #aaa; letter-spacing: 1px;">TRACKING THE GLITCHES IN OUR REALITY</div>
</div>
</div>""", unsafe_allow_html=True)
    with c2:
        query = st.text_input("SEARCH FREQUENCY...", label_visibility="collapsed", placeholder="Search reality...")
        if query:
            if query.strip().upper() == "ARCHITECT":
                st.session_state['page'] = 'admin'
                st.rerun()
            elif query.strip().upper() == "RESET":
                 st.session_state['posts'] = [] # Clear posts
                 st.rerun()
            else:
                 # Search Filter Logic
                 results_count = 0
                 for p in st.session_state['posts']:
                     if query.lower() in p['status'].lower() or query.lower() in p['tags']:
                         results_count += 1
                 
                 if results_count > 0:
                     st.toast(f"FOUND {results_count} MATCHES FOR '{query.upper()}'")
                     # Store filter in session state if we wanted to implement actual filtering on feed
                     # For now just show toast to confirm it works
                 else:
                     st.toast(f"Searching frequency: {query}... SIGNAL WEAK (NO MATCHES).")
    with c3:
        if st.button("💬", key="msg_icon"):
            st.session_state['page'] = 'messages'
            st.rerun()
            
    st.markdown("---")

def bottom_nav():
    """Bottom Navigation Bar (Tabs)"""
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🏠 HOME", use_container_width=True, key="nav_home"):
            st.session_state['page'] = 'feed'
            st.rerun()
    with c2:
        if st.button("�️ OBSERVERS", use_container_width=True, key="nav_observers"):
            st.session_state['page'] = 'observers'
            st.rerun()
    with c3:
        if st.button("🔔 NOTIFICATIONS", use_container_width=True, key="nav_notif"):
            st.session_state['page'] = 'notifications'
            st.rerun()
    with c4:
        if st.button("👤 PROFILE", use_container_width=True, key="nav_profile"):
            st.session_state['page'] = 'profile'
            st.rerun()

def anomaly_categories_section():
    """Horizontal Anomaly Categories"""
    st.markdown("**CLASSIFIED ARCHIVES**")
    
    # Custom CSS for the category cards to ensure they look like buttons/cards
    st.markdown("""
    <style>
    .category-card {
        background: rgba(0, 20, 0, 0.6);
        border: 1px solid #00FF41;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    .category-card:hover {
        background: rgba(0, 255, 65, 0.1);
        box-shadow: 0 0 10px #00FF41;
    }
    .cat-title {
        font-size: 0.8em; 
        font-weight: bold; 
        color: #FFF; 
        margin-bottom: 5px;
    }
    .cat-desc {
        font-size: 0.6em; 
        color: #00FF41;
    }
    .cat-icon {
        font-size: 1.5em;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(len(st.session_state['categories']))
    for i, cat in enumerate(st.session_state['categories']):
        with cols[i]:
            # Using HTML for better layout control of Title + Subtitle
            st.markdown(f"""<div class="category-card">
<div class="cat-icon">{cat['icon']}</div>
<div class="cat-title">{cat['title']}</div>
<div class="cat-desc">{cat['desc']}</div>
</div>""", unsafe_allow_html=True)
            # Invisible button overlay for interaction if needed
            if st.button("OPEN", key=f"cat_btn_{i}"):
                 st.toast(f"Accessing {cat['title']} Archive...")
                 
    st.markdown("---")

def feed_view():
    """The Global Superposition Feed"""
    app_bar()
    anomaly_categories_section()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h2 class="neon-green">GLOBAL SUPERPOSITION FEED</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("REPORT BREACH +"):
            st.session_state['page'] = 'post'
            st.rerun()

    for post in st.session_state['posts']:
        with st.container():
            c1, c2 = st.columns([2, 1])
            with c1:
                # Header: Pic, Name, Time
                st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <div style="width: 30px; height: 30px; background: #333; border-radius: 50%; margin-right: 10px; border: 1px solid #00FF41;"></div>
                    <div>
                        <span class="neon-green" style="font-weight: bold;">@{post['user']}</span><br>
                        <span style="color: #555; font-size: 0.8em;">T-{post['time']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Body: Media & Text
                div_style = "background: #000; height: 200px; display: flex; align-items: center; justify-content: center; border: 1px solid #222; margin-bottom: 10px;"
                st.markdown(f"""
                <div style="{div_style}">
                    <span style="color: #333;">[VIDEO FEED ENCRYPTED]</span>
                </div>
                <p>{post['status']}</p>
                <div style="font-size: 0.8em; color: #555; margin-top: 10px;">TAGS: {", ".join(post['tags'])}</div>
                """, unsafe_allow_html=True)
                
            with c2:
                # Footer: Voting
                st.markdown(f"**RESONANCE METER**")
                render_resonance_meter(post['protons'], post['electrons'], post['neutrals'])
                
                st.markdown("<div class='atom-container'>", unsafe_allow_html=True)
                ac1, ac2, ac3 = st.columns(3)
                with ac1:
                    if st.button("Real (+)", key=f"p_{post['id']}"):
                         post['protons'] += 1
                         st.toast("REALITY CONFIRMED (+)")
                with ac2:
                    if st.button("Fake (-)", key=f"e_{post['id']}"):
                         post['electrons'] += 1
                         st.toast("DECOHERENCE DETECTED (-)")
                with ac3:
                    if st.button("💬", key=f"c_btn_{post['id']}"):
                         st.toast("Opening Comment Stream...")
                st.markdown("</div>", unsafe_allow_html=True)
    
    bottom_nav()

def post_view():
    st.markdown('<h2 class="neon-green">LOG NEW BREACH</h2>', unsafe_allow_html=True)
    
    if st.button("← CANCEL"):
        st.session_state['page'] = 'feed'
        st.rerun()

    with st.form("breach_form"):
        status_text = st.text_area("STATUS REPORT", placeholder="Describe the anomaly...")
        tags_input = st.text_input("TAGS (comma separated)", placeholder="time, glitch, shadow")
        st.file_uploader("UPLOAD EVIDENCE", type=['mp4', 'jpg', 'png'])
        
        if st.form_submit_button("TRANSMIT TO FEED"):
            # Mock saving post
            new_tags = [t.strip() for t in tags_input.split(",") if t.strip()]
            new_post = {
                "id": len(st.session_state['posts']) + 101,
                "user": st.session_state['user']['name'],
                "time": time.strftime("%H:%M"),
                "status": status_text,
                "tags": new_tags,
                "protons": 1,
                "electrons": 0,
                "neutrals": 0,
                "comments": []
            }
            st.session_state['posts'].insert(0, new_post)
            
            # Run Entanglement Algorithm
            matches = check_entanglement(status_text, new_tags)
            if matches:
                st.session_state['entanglement_alert'] = matches
                add_notification("entanglements", f"SYNC DETECTED: {len(matches)} matches found for your breach.")
            
            st.success("BREACH LOGGED.")
            time.sleep(1)
            st.session_state['page'] = 'feed'
            st.rerun()

def profile_view():
    app_bar()
    st.markdown('<h2 class="neon-green">LOCAL SUPERPOSITION FEED (PROFILE)</h2>', unsafe_allow_html=True)
    
    user = st.session_state['user']
    
    # Profile Header
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f"""
        <div class="profile-pic-container">
             <img src="{user.get('profile_pic', 'https://via.placeholder.com/150')}" class="profile-pic">
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.title(user.get('name', 'Agent'))
        st.markdown(f"**Resonance Score:** {user.get('resonance_score', 0)}")
        st.markdown(f"**Bio:** {user.get('bio', 'No bio encrypted.')}")
        
    with st.expander("EDIT PROFILE"):
        new_bio = st.text_area("Update Bio", user.get('bio', ''))
        new_pic = st.file_uploader("Update Profile Picture", type=['jpg', 'png'])
        if st.button("SAVE PROFILE"):
            st.session_state['user']['bio'] = new_bio
            if new_pic:
                st.session_state['user']['profile_pic'] = "https://via.placeholder.com/150/00FF41/000000?text=IMG"
            st.success("PROFILE UPDATED")
            st.rerun()
            
    st.markdown("### BREACH HISTORY")
    # Filter posts by this user (Mock logic)
    my_posts = [p for p in st.session_state['posts'] if p['user'] == user.get('name')]
    
    if not my_posts:
        st.info("No breaches logged yet.")
    else:
        for post in my_posts:
             render_glass_card(f"""<div style="margin-bottom: 5px;">
<span style="color: #888;">{post['time']}</span>
</div>
<p>{post['status']}</p>
<div style="color: #00FF41;">Protons: {post['protons']} | Electrons: {post['electrons']}</div>""")
    
    bottom_nav()

def observers_view():
    app_bar()
    st.markdown('<h2 class="neon-green">ACTIVE ENTANGLEMENTS (OBSERVERS)</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["CONNECTED OBSERVERS", "ENCRYPTED CHANNEL"])
    
    with tab1:
        # Mock Pending Requests
        if 'pending_observers' not in st.session_state:
            st.session_state['pending_observers'] = ["Cipher_01"]
            
        if st.session_state['pending_observers']:
            st.markdown("### PENDING SYNCS")
            for p_user in st.session_state['pending_observers']:
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**{p_user}** requests observer status.")
                with c2:
                    if st.button("ACCEPT", key=f"accept_{p_user}"):
                        add_notification("observers", f"Entanglement confirmed with {p_user}.")
                        st.session_state['pending_observers'].remove(p_user)
                        st.rerun()
                        
        st.markdown("### ONLINE OBSERVERS")
        cols = st.columns(3)
        with cols[0]:
            st.image("https://via.placeholder.com/100/00FF41/000000?text=AI", width=80)
            st.caption("THE OBSERVER")
            if st.button("MESSAGE", key="msg_ai"):
                 st.session_state['active_contact'] = "THE OBSERVER"
                 st.rerun()
        with cols[1]:
            st.image("https://via.placeholder.com/100/00FF41/000000?text=CW", width=80)
            st.caption("Chronos_Walker")
            if st.button("MESSAGE", key="msg_cw"):
                 st.session_state['active_contact'] = "Chronos_Walker"
                 st.rerun()
        with cols[2]:
            st.image("https://via.placeholder.com/100/FF003C/000000?text=GH", width=80)
            st.caption("Glitch_Hunter")
            if st.button("MESSAGE", key="msg_gh"):
                 st.session_state['active_contact'] = "Glitch_Hunter"
                 st.rerun()
            
    with tab2:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### SELECT FREQUENCY")
            contacts = ["THE OBSERVER", "Chronos_Walker", "Glitch_Hunter", "Morpheus"]
            
            # Use session state to persist selection from tab1
            default_ix = 0
            if 'active_contact' in st.session_state and st.session_state['active_contact'] in contacts:
                default_ix = contacts.index(st.session_state['active_contact'])
                
            active_contact = st.radio("Channel", contacts, index=default_ix, label_visibility="collapsed")
            st.session_state['active_contact'] = active_contact # Sync back
        
        with col2:
            st.markdown(f"### LINKED: {active_contact}")
            
            # Chat History Mock Logic
            if active_contact == "THE OBSERVER":
                 chat_history = st.session_state.get('ai_chat_history', [])
                 if not chat_history:
                     chat_history.append({"role": "system", "content": "I AM THE OBSERVER. I AM LISTENING."})
                     st.session_state['ai_chat_history'] = chat_history
                 
                 chat_container = st.container(height=300)
                 for msg in chat_history:
                     color = "#00FF41" if msg['role'] == "system" else "#FFF"
                     align = "left" if msg['role'] == "system" else "right"
                     chat_container.markdown(f"<div style='text-align: {align}; color: {color}; margin-bottom: 5px;'>[{msg['role'].upper()}] {msg['content']}</div>", unsafe_allow_html=True)
                 
                 # Input for AI
                 c_input, c_btn = st.columns([3, 1])
                 with c_input:
                     ai_msg = st.text_input("Query the System", key="ai_input", label_visibility="collapsed")
                 with c_btn:
                     if st.button("TRANSMIT"):
                         if ai_msg:
                             st.session_state['ai_chat_history'].append({"role": "user", "content": ai_msg})
                             # AI Reply
                             reply = get_ai_response(ai_msg)
                             st.session_state['ai_chat_history'].append({"role": "system", "content": reply})
                             st.rerun()
                             
            else:
                # Standard Chat History Mock
                st.markdown("""
                <div style="height: 300px; overflow-y: scroll; border: 1px solid #333; padding: 10px; margin-bottom: 10px;">
                    <div style="color: #888;">[14:05] SYSTEM: Channel Open.</div>
                    <div style="color: #00FF41;">[14:06] Me: Did you see the flash?</div>
                    <div style="color: #FFF;">[14:07] Chronos_Walker: Yes. It matched my reading.</div>
                </div>
                """, unsafe_allow_html=True)
                
                c_input, c_btn = st.columns([3, 1])
                with c_input:
                    msg_input = st.text_input("Payload", key="msg_input", label_visibility="collapsed")
                with c_btn:
                    if st.button("SEND"):
                        st.write("Sending...") # Mock
                        add_notification("messages", f"Transmission sent to {active_contact}")
                        time.sleep(0.5)
                        st.rerun()
    
    # Bottom Right Observer Eye (Visual Only)
    st.markdown("""
    <div style="position: fixed; bottom: 80px; right: 20px; font-size: 2em; animation: pulse-green 3s infinite; cursor: pointer;" title="THE OBSERVER IS WATCHING">
        👁️
    </div>
    """, unsafe_allow_html=True)
    
    bottom_nav()

def notifications_view():
    app_bar()
    st.markdown('<h2 class="neon-green">NOTIFICATIONS (THE FOLD)</h2>', unsafe_allow_html=True)
    
    # --- Settings Section ---
    with st.expander("⚙️ NOTIFICATION CONFIGURATION"):
        st.markdown("Manage your neural link filters.")
        settings = st.session_state['notification_settings']
        
        c1, c2 = st.columns(2)
        with c1:
            settings['entanglements'] = st.checkbox("Entanglement Alerts", value=settings['entanglements'])
            settings['messages'] = st.checkbox("Secure Messages", value=settings['messages'])
        with c2:
            settings['brand'] = st.checkbox("System/Brand Updates", value=settings['brand'])
            settings['friends'] = st.checkbox("Friend Syncs", value=settings['friends'])
            
        st.session_state['notification_settings'] = settings

    # --- Live Alerts ---
    if st.session_state['entanglement_alert']:
        render_entanglement_alert(st.session_state['entanglement_alert'])
        if st.button("ACKNOWLEDGE SYNC"):
            st.session_state['entanglement_alert'] = None
            add_notification("entanglements", "Entanglement Alert Acknowledged.")
            st.rerun()

    # --- Notification Stream ---
    st.markdown("### INCOMING DATA STREAM")
    
    if not st.session_state['notifications']:
        st.info("No active notifications. The void is silent.")
    else:
        for notif in st.session_state['notifications']:
            # Style based on type
            border_color = "#00FF41" # Default Green
            if notif['type'] == 'brand': border_color = "#0088FF" # Blue
            if notif['type'] == 'entanglements': border_color = "#FF003C" # Red
            
            read_status = "opacity: 0.6;" if notif['read'] else "opacity: 1;"
            
            st.markdown(f"""<div class="glass-card" style="border-left: 4px solid {border_color}; {read_status} padding: 10px; margin-bottom: 10px;">
<div style="display: flex; justify-content: space-between;">
<span style="color: {border_color}; font-weight: bold;">[{notif['type'].upper()}]</span>
<span style="color: #666; font-family: monospace;">{notif['time']}</span>
</div>
<p style="margin: 5px 0;">{notif['message']}</p>
</div>""", unsafe_allow_html=True)
            
            # Mark as read implicitly by rendering (or could add a button)
            notif['read'] = True
            
    bottom_nav()

def admin_view():
    app_bar()
    st.markdown('<h2 class="warning-red">ARCHITECT DASHBOARD</h2>', unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← EXIT GOD MODE"):
            st.session_state['page'] = 'feed'
            st.rerun()
    with c2:
        st.warning("⚠ ROOT ACCESS GRANTED ⚠")

    st.markdown("---")

    with st.expander("DEPLOYMENT CONTROLS", expanded=True):
        st.markdown("### SYSTEM READINESS")
        deploy_ready = st.checkbox("ARM DEPLOYMENT PROTOCOLS", value=True)
        if deploy_ready:
            st.success("SYSTEM IS READY FOR PUBLIC INJECTION.")
            st.markdown("*The interface is locked to your bio-signature. No other entities can access this panel.*")
        else:
            st.error("SYSTEM LOCKED. SANDBOX MODE ONLY.")

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### ENTITY MANAGEMENT")
        with st.expander("REPORTED: ID #9921", expanded=True):
            st.write("**User:** Void_Runner")
            st.write("**Reason:** Obscene data injection")
            if st.button("EXTERMINATE ENTITY", type="primary"):
                st.success("ENTITY DELETED.")
                add_notification("brand", "SECURITY ALERT: Malicious entity purged from the Fold.")
                time.sleep(1)
                st.rerun()

    with col_b:
        st.markdown("### GLOBAL BROADCAST")
        with st.expander("SEND SYSTEM MESSAGE", expanded=True):
            broadcast_msg = st.text_input("Transmission Content", placeholder="ALERT: REALITY SHIFT...")
            if st.button("BROADCAST TO ALL NODES"):
                if broadcast_msg:
                    add_notification("brand", f"SYSTEM BROADCAST: {broadcast_msg}")
                    st.success("TRANSMISSION SENT.")
                    time.sleep(1)
                    st.rerun()
    
    bottom_nav()

def setup_profile_view():
    """First-time user setup"""
    render_glass_card("""<h2 class="neon-green" style="text-align: center;">IDENTITY ENCRYPTION</h2>
<p style="text-align: center; color: #888;">INITIALIZE YOUR AVATAR</p>
<hr style="border-color: #333;">""")
    
    with st.form("setup_form"):
        username = st.text_input("CODENAME (USERNAME)", value="Agent_")
        bio = st.text_area("BIO-DATA (SHORT DESCRIPTION)", placeholder="Ex: Time traveler stuck in 2024.")
        uploaded_file = st.file_uploader("UPLOAD AVATAR", type=['jpg', 'png'])
        
        if st.form_submit_button("ESTABLISH IDENTITY"):
            st.session_state['user']['name'] = username
            st.session_state['user']['bio'] = bio
            
            # Handle profile pic
            if uploaded_file:
                # In Streamlit, we can't easily save to disk in a hosted environment without persistence,
                # but we can use the bytes directly or encoded.
                # For this mock, we will continue to use the placeholder but visually acknowledge the upload.
                st.session_state['user']['profile_pic'] = "https://via.placeholder.com/150/00FF41/000000?text=" + username[:2].upper()
            else:
                st.session_state['user']['profile_pic'] = "https://via.placeholder.com/150/00FF41/000000?text=" + username[:2].upper()
            
            st.session_state['setup_complete'] = True
            st.success("IDENTITY CONFIRMED.")
            time.sleep(1)
            st.rerun()

# --- MAIN CONTROLLER ---

if not st.session_state['initialized']:
    void_layer_view()
else:
    if not auth.check_auth():
        login_view()
    elif 'setup_complete' not in st.session_state:
         # Check if we need setup
         setup_profile_view()
    else:
        # Check Global Alerts (from Post View)
        if st.session_state['entanglement_alert']:
            render_entanglement_alert(st.session_state['entanglement_alert'])
            # Create a centered button to dismiss
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                if st.button("ACKNOWLEDGE SYNC", key="ack_alert_main"):
                    st.session_state['entanglement_alert'] = None
                    st.rerun()
            
        # Router
        if st.session_state['page'] == 'feed':
            feed_view()
        elif st.session_state['page'] == 'post':
            post_view()
        elif st.session_state['page'] == 'profile':
            profile_view()
        elif st.session_state['page'] == 'observers':
            observers_view()
        elif st.session_state['page'] == 'messages': # Keep for backward compat or direct link
            observers_view()
        elif st.session_state['page'] == 'notifications':
            notifications_view()
        elif st.session_state['page'] == 'fold': # Keep for backward compat
            notifications_view()
        elif st.session_state['page'] == 'admin':
            admin_view()
