import streamlit as st
import time
import secrets

# Mock User Database
USERS = {
    "admin": "password123",
    "agent_smith": "matrix",
    "void_runner": "glitch",
    "architect": "matrix_source_code"
}

def verify_login(username, password):
    """Verifies username and password against mock DB"""
    if username in USERS and USERS[username] == password:
        return True
    return False

def login_user(username, remember_me=False):
    """Sets session state for logged in user"""
    st.session_state['logged_in'] = True
    st.session_state['user'] = {
        'name': username,
        'resonance_score': 0, # Default, will load from profile later
        'bio': 'Encrypted'
    }
    
    if remember_me:
        # Simple "Remember Me" implementation using Query Params
        # In a real app, use a secure HTTP-only cookie
        token = secrets.token_urlsafe(16)
        # Store token mapping (Mock)
        st.session_state['auth_token'] = token
        st.query_params['auth_token'] = token
    else:
        # Clear token if not remembering
        if 'auth_token' in st.query_params:
            del st.query_params['auth_token']

def check_auth():
    """Checks if user is logged in via Session or Token"""
    
    # 1. Check Session State
    if st.session_state.get('logged_in', False):
        return True
        
    # 2. Check "Remember Me" Token (Simple Mock)
    # In reality, you'd validate this token against a DB
    query_params = st.query_params
    if 'auth_token' in query_params:
        token = query_params['auth_token']
        # For this mock, we just accept any token that looks like ours (length check)
        # and auto-login as a default user if valid
        if len(token) > 10: 
            st.session_state['logged_in'] = True
            st.session_state['user'] = {
                'name': 'Returning_Agent',
                'resonance_score': 88,
                'bio': 'Auto-Login Successful'
            }
            st.toast("AUTO-LOGIN SUCCESSFUL. WELCOME BACK.")
            return True
            
    return False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user'] = {}
    if 'auth_token' in st.query_params:
        del st.query_params['auth_token']
    st.rerun()
