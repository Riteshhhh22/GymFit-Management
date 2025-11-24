from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'  # VULNERABLE: Weak secret key!

# Database helper function
def get_db_connection():
    conn = sqlite3.connect('gym.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# VULNERABILITY 1: SQL INJECTION in Login
# ==========================================
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash password with MD5 (VULNERABLE: Weak hashing!)
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        # VULNERABLE: Direct string concatenation - SQL Injection possible!
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'"
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # VULNERABILITY 2: BROKEN AUTHENTICATION
            # Weak session management - predictable session tokens
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['logged_in'] = True
            
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    
    return render_template('login.html')

# ==========================================
# Dashboard Route
# ==========================================
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get statistics
    members_count = conn.execute('SELECT COUNT(*) as count FROM members').fetchone()['count']
    trainers_count = conn.execute('SELECT COUNT(*) as count FROM trainers').fetchone()['count']
    
    conn.close()
    
    return render_template('dashboard.html', 
                         members_count=members_count,
                         trainers_count=trainers_count)

# ==========================================
# VULNERABILITY 3: XSS in Member Management
# ==========================================
@app.route('/members')
def members():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Search functionality - VULNERABLE to SQL Injection!
    search = request.args.get('search', '')
    
    if search:
        # VULNERABLE: SQL Injection in search
        query = f"SELECT * FROM members WHERE name LIKE '%{search}%' OR email LIKE '%{search}%'"
        members = conn.execute(query).fetchall()
    else:
        members = conn.execute('SELECT * FROM members').fetchall()
    
    conn.close()
    
    # Members data will be displayed without escaping (XSS vulnerability in template)
    return render_template('members.html', members=members, search=search)

# ==========================================
# Add Member (XSS vulnerability)
# ==========================================
@app.route('/members/add', methods=['POST'])
def add_member():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    membership_type = request.form['membership_type']
    notes = request.form['notes']  # VULNERABLE: No XSS protection!
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO members (name, email, phone, membership_type, join_date, notes)
        VALUES (?, ?, ?, ?, date('now'), ?)
    ''', (name, email, phone, membership_type, notes))
    conn.commit()
    conn.close()
    
    flash('Member added successfully!', 'success')
    return redirect(url_for('members'))

# ==========================================
# VULNERABILITY 4: IDOR - Insecure Direct Object Reference
# ==========================================
@app.route('/profile/<int:user_id>')
def profile(user_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # VULNERABLE: No authorization check!
    # Any logged-in user can view any profile by changing the user_id
    conn = get_db_connection()
    
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get member details if user is a member
    member = conn.execute('SELECT * FROM members WHERE email LIKE ?', 
                         (f'%{user["username"]}%',)).fetchone()
    
    conn.close()
    
    return render_template('profile.html', user=user, member=member)

# ==========================================
# Trainers Management
# ==========================================
@app.route('/trainers')
def trainers():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    trainers = conn.execute('SELECT * FROM trainers').fetchall()
    conn.close()
    
    return render_template('trainers.html', trainers=trainers)

# ==========================================
# Logout
# ==========================================
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ==========================================
# Run Application
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
