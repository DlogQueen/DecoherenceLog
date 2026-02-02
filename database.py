import sqlite3
import datetime

DB_NAME = "decoherence.db"

def init_db():
    """Initialize the SQLite database with the necessary tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # USERS TABLE
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        avatar_url TEXT,
        resonance_score INTEGER DEFAULT 0,
        role TEXT DEFAULT 'user',
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # POSTS TABLE
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
        neutrons INTEGER DEFAULT 0,
        integrity_status TEXT DEFAULT 'active', -- active, reported, quarantined
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    # VOTES TABLE (To prevent double voting and track history)
    c.execute('''CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        post_id INTEGER,
        vote_type TEXT, -- proton, electron, neutron
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, post_id)
    )''')
    
    # ENTANGLEMENTS TABLE
    c.execute('''CREATE TABLE IF NOT EXISTS entanglements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id_1 INTEGER,
        user_id_2 INTEGER,
        post_id_1 INTEGER,
        post_id_2 INTEGER,
        match_reason TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(username, email, avatar_url=""):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, email, avatar_url) VALUES (?, ?, ?)", 
                  (username, email, avatar_url))
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        return None # User exists
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user

def create_post(user_id, username, status_text, media_path, media_type, tags):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO posts (user_id, username, status_text, media_path, media_type, tags) 
                 VALUES (?, ?, ?, ?, ?, ?)""", 
              (user_id, username, status_text, media_path, media_type, tags))
    conn.commit()
    post_id = c.lastrowid
    conn.close()
    return post_id

def get_all_posts(include_hidden=False):
    conn = get_db_connection()
    query = "SELECT * FROM posts ORDER BY created_at DESC"
    if not include_hidden:
        query = "SELECT * FROM posts WHERE integrity_status = 'active' ORDER BY created_at DESC"
    posts = conn.execute(query).fetchall()
    conn.close()
    return [dict(p) for p in posts]

def get_reported_posts():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts WHERE integrity_status = 'reported' ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(p) for p in posts]

def update_post_status(post_id, status):
    conn = get_db_connection()
    conn.execute("UPDATE posts SET integrity_status = ? WHERE id = ?", (status, post_id))
    conn.commit()
    conn.close()

def add_vote(user_id, post_id, vote_type):
    """
    Adds a vote and updates the post counts. 
    Returns True if vote was successful, False if changed/removed (logic simplified for prototype).
    """
    conn = get_db_connection()
    c = conn.cursor()
    
    # Check if vote exists
    existing = c.execute("SELECT vote_type FROM votes WHERE user_id = ? AND post_id = ?", (user_id, post_id)).fetchone()
    
    if existing:
        # If same vote, ignore or toggle off? Let's say we ignore for now to keep it simple
        if existing['vote_type'] == vote_type:
            conn.close()
            return False
        
        # If different, remove old vote count
        old_type = existing['vote_type']
        if old_type == 'proton':
            c.execute("UPDATE posts SET protons = protons - 1 WHERE id = ?", (post_id,))
        elif old_type == 'electron':
            c.execute("UPDATE posts SET electrons = electrons - 1 WHERE id = ?", (post_id,))
        elif old_type == 'neutron':
            c.execute("UPDATE posts SET neutrons = neutrons - 1 WHERE id = ?", (post_id,))
            
        c.execute("UPDATE votes SET vote_type = ? WHERE user_id = ? AND post_id = ?", (vote_type, user_id, post_id))
    else:
        c.execute("INSERT INTO votes (user_id, post_id, vote_type) VALUES (?, ?, ?)", (user_id, post_id, vote_type))
    
    # Add new vote count
    if vote_type == 'proton':
        c.execute("UPDATE posts SET protons = protons + 1 WHERE id = ?", (post_id,))
    elif vote_type == 'electron':
        c.execute("UPDATE posts SET electrons = electrons + 1 WHERE id = ?", (post_id,))
    elif vote_type == 'neutron':
        c.execute("UPDATE posts SET neutrons = neutrons + 1 WHERE id = ?", (post_id,))
        
    conn.commit()
    conn.close()
    return True

def check_for_entanglements(new_post_id, tags, timeframe_hours=24):
    """
    Scans for similar posts within the timeframe.
    Returns a list of matching post IDs.
    """
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get the new post details
    new_post = c.execute("SELECT * FROM posts WHERE id = ?", (new_post_id,)).fetchone()
    if not new_post:
        return []

    # Parse tags
    tag_list = [t.strip().lower() for t in tags.split(',')]
    if not tag_list:
        return []
        
    # Construct query for tag matching
    # This is a basic "OR" match on tags.
    # In a real app, we'd use a more complex search.
    query = "SELECT * FROM posts WHERE id != ? AND created_at >= datetime('now', ?)"
    params = [new_post_id, f'-{timeframe_hours} hours']
    
    candidates = c.execute(query, params).fetchall()
    matches = []
    
    for post in candidates:
        post_tags = [t.strip().lower() for t in post['tags'].split(',')]
        # Check intersection
        if set(tag_list) & set(post_tags):
            matches.append(post)
            # Record Entanglement
            c.execute("INSERT INTO entanglements (user_id_1, user_id_2, post_id_1, post_id_2, match_reason) VALUES (?, ?, ?, ?, ?)",
                      (new_post['user_id'], post['user_id'], new_post_id, post['id'], "Tag Resonance"))
    
    conn.commit()
    conn.close()
    return matches
