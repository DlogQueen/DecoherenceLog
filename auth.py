import streamlit as st
import database

# Mock Authentication for immediate use
def check_password():
    """Returns `True` if the user had the correct password."""
    return st.session_state.get("authenticated", False)

def login_user(username, email="agent@decoherence.log"):
    st.session_state["authenticated"] = True
    st.session_state["username"] = username
    st.session_state["email"] = email
    
    # Ensure user exists in DB
    user = database.get_user_by_email(email)
    if not user:
        uid = database.create_user(username, email)
        st.session_state["user_id"] = uid
        st.session_state["role"] = "user"
    else:
        st.session_state["user_id"] = user['id']
        st.session_state["role"] = user['role']

def logout_user():
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["user_id"] = None
    st.session_state["role"] = None

def get_current_user():
    if st.session_state.get("authenticated"):
        return {
            "id": st.session_state.get("user_id"),
            "username": st.session_state.get("username"),
            "email": st.session_state.get("email"),
            "role": st.session_state.get("role")
        }
    return None

def is_admin():
    user = get_current_user()
    return user and user['role'] == 'admin'

# --- GOOGLE AUTH PLACEHOLDER ---
# In a production environment, we would use:
# from google_auth_oauthlib.flow import Flow
# But for this prototype, we simulate the "Handshake".

def google_login_btn():
    """
    Renders the Google Login button. 
    If secrets are missing, it falls back to a simulated login.
    """
    # Check for secrets
    if "google" in st.secrets:
        # Implement real OAuth flow here if keys exist
        pass
    
    # Simulation for the prototype
    if st.button("AUTHENTICATE BIOMETRICS [GOOGLE LINK]", type="primary", use_container_width=True):
        return True
    return False
