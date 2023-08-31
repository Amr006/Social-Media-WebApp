def connect_to_database(name='database.db'):
    import sqlite3
    return sqlite3.connect(name, check_same_thread=False)

def init_db(connection):
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE, 
    password TEXT NOT NULL
    )   
    ''') 
    
    connection.commit()

def add_user(connection, username, password):
    cursor = connection.cursor()
    query = 'INSERT INTO users (username, password) VALUES (?, ?)'
    cursor.execute(query, (username, password))
    connection.commit()

def get_user_by_username(connection, username):
    cursor = connection.cursor()
    query = 'SELECT * FROM users WHERE username = ?' 
    cursor.execute(query, (username,))
    return cursor.fetchone()

def init_Post_db(connection):

    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gadgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                image_url TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
    ''')
    connection.commit()
