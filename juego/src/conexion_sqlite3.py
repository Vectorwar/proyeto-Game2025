import sqlite3

"""try: 
    mi_conexion=sqlite3.connect("database/scoredb")
    print("Conexion exitosa")
except Exception as ex:
    print(ex)"""

def init_database():
    """Initialize the SQLite database and create the scores table"""
    conn = sqlite3.connect('database/scoredb')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_score():
        """Save a score to the database"""
        conn = sqlite3.connect('database/scoredbdb')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO scores (player_name, score, date) VALUES (?, ?, ?)',
                   (player_name, score, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

def save_score(player_name, score):
    """Save a score to the database"""
    conn = sqlite3.connect('database/scoredb')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO scores (player_name, score, date) VALUES (?, ?, ?)',
                   (player_name, score, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()