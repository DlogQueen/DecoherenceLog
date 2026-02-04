import sqlite3
import datetime
import os

DB_NAME = "decoherence.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Posts Table
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        status_text TEXT,
        media_path TEXT,
        media_type TEXT,
        tags TEXT,
        protons INTEGER DEFAULT 0,
        electrons INTEGER DEFAULT 0,
        neutrals INTEGER DEFAULT 0,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Votes Table
    c.execute('''CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        post_id INTEGER,
        vote_type TEXT
    )''')
    
    conn.commit()
    conn.close()

def get_all_posts():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE status='active' ORDER BY created_at DESC")
    posts = [dict(row) for row in c.fetchall()]
    conn.close()
    return posts

def create_post(user_id, username, status, media_path, media_type, tags):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO posts (user_id, username, status_text, media_path, media_type, tags) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, username, status, media_path, media_type, tags))
    post_id = c.lastrowid
    conn.commit()
    conn.close()
    return post_id

def add_vote(user_id, post_id, vote_type):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO votes (user_id, post_id, vote_type) VALUES (?, ?, ?)", (user_id, post_id, vote_type))
    
    if vote_type == 'proton':
        c.execute("UPDATE posts SET protons = protons + 1 WHERE id = ?", (post_id,))
    elif vote_type == 'electron':
        c.execute("UPDATE posts SET electrons = electrons + 1 WHERE id = ?", (post_id,))
        
    conn.commit()
    conn.close()

def check_for_entanglements(new_post_id, new_tags):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    tag_list = [t.strip() for t in new_tags.split(',')]
    matches = []
    
    for tag in tag_list:
        c.execute("SELECT username FROM posts WHERE tags LIKE ? AND id != ?", (f'%{tag}%', new_post_id))
        rows = c.fetchall()
        for row in rows:
            if row['username'] not in matches:
                matches.append(row['username'])
                
    conn.close()
    return matches

def get_reported_posts():
    return get_all_posts()

def update_post_status(post_id, status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE posts SET status = ? WHERE id = ?", (status, post_id))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def create_user(username, email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
    uid = c.lastrowid
    conn.commit()
    conn.close()
    return uid
