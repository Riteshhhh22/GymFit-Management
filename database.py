import sqlite3
import hashlib

def init_db():
    """Initialize the database with tables and sample data"""
    conn = sqlite3.connect('gym.db')
    cursor = conn.cursor()
    
    # Create Members table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            membership_type TEXT,
            join_date DATE,
            notes TEXT
        )
    ''')
    
    # Create Trainers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trainers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            specialization TEXT,
            experience_years INTEGER
        )
    ''')
    
    # Create Users table (for login - VULNERABLE!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            session_token TEXT
        )
    ''')
    
    # Insert sample admin user (WEAK PASSWORD - Vulnerability!)
    # Password is 'admin123' - stored as plain MD5 hash (VULNERABLE!)
    admin_pass = hashlib.md5('admin123'.encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES ('admin', ?, 'admin')
    ''', (admin_pass,))
    
    # Insert sample member user
    member_pass = hashlib.md5('member123'.encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES ('john_doe', ?, 'member')
    ''', (member_pass,))
    
    # Insert sample members
    sample_members = [
        ('John Doe', 'john@email.com', '555-0101', 'Premium', '2024-01-15', 'Regular member'),
        ('Jane Smith', 'jane@email.com', '555-0102', 'Basic', '2024-02-20', 'Prefers morning sessions'),
        ('Mike Johnson', 'mike@email.com', '555-0103', 'Premium', '2024-03-10', 'Interested in weightlifting'),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO members (name, email, phone, membership_type, join_date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_members)
    
    # Insert sample trainers
    sample_trainers = [
        ('Sarah Connor', 'sarah@gymfit.com', 'Strength Training', 5),
        ('Tom Hardy', 'tom@gymfit.com', 'Cardio & HIIT', 3),
        ('Emma Watson', 'emma@gymfit.com', 'Yoga & Pilates', 7),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO trainers (name, email, specialization, experience_years)
        VALUES (?, ?, ?, ?)
    ''', sample_trainers)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")
    print("📝 Default login credentials:")
    print("   Username: admin")
    print("   Password: admin123")

if __name__ == '__main__':
    init_db()
