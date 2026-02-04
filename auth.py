import streamlit as st
import time

def mock_login():
    """Simulates Google OAuth Login"""
    st.session_state['logged_in'] = True
    st.session_state['user'] = {
        'name': 'Agent_Smith',
        'email': 'agent@matrix.com',
        'resonance_score': 42
    }

def check_auth():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    return st.session_state['logged_in']

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user'] = {}
    st.rerun()
