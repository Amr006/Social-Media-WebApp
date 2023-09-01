def connect_to_database(name='database.db'):
    import sqlite3
    return sqlite3.connect(name, check_same_thread=False)

def init_users(connection):
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

def get_user_by_user_id(connection, username):
    cursor = connection.cursor()
    query = 'SELECT * FROM users WHERE username = ?' 
    cursor.execute(query, (username,))
    return cursor.fetchone()

def init_posts(connection):

    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS POSTS (
                user_id INTEGER NOT NULL,
                description TEXT,
                image_url TEXT,
                post_id INTEGER NOT NULL PRIMARY KEY,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
    ''')
    connection.commit()

def add_Post(connection, user_id, description, image_url, post_id):
    cursor = connection.cursor()
    query = 'INSERT INTO POSTS (user_id, description, image_url, post_id)VALUES(?, ?, ?, ?)'
    cursor.execute(query, user_id, description, image_url, post_id)
    connection.commit()
    
def get_all_posts(connection):
    cursor = connection.cursor()
    query = 'SELECT p.*, c.id AS comment_id, c.content AS comment_content FROM POSTS p LEFT JOIN COMMENTS c ON p.post_id = c.comment_id'
    cursor.execute(query)
    
    posts = {}
    for row in cursor.fetchall():
        post_id = row[3]
        if post_id not in posts:
            posts[post_id] = {
                'post_id': post_id,
                'user_id': row[0],
                'description': row[1],
                'image_url': row[2],
                'comments': []
            }
        
        if row[4] is not None:
            posts[post_id]['comments'].append({
                'comment_id': row[5],
                'comment_content': row[6]
            })
    
    return list(posts.values())


def init_comments(connection):
     
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS COMMENTS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT not null,
                comment_id INTEGER NOT NULL UNIQUE,
                FOREIGN KEY (comment_id) REFERENCES POSTS (post_id)
            )
    ''')
    connection.commit()

def add_comment_to_db(connection, user_id, comment_content, comment_id):
    cursor = connection.cursor()
    query = 'INSERT INTO COMMENTS (user_id, comment_content, comment_id) VALUES(?, ?, ?)'
    cursor.execute(query, (user_id, comment_content, comment_id))

    connection.commit()

def get_post_by_post_id(connection, post_id):
    cursor = connection.cursor()

    query = '''
    SELECT p.*, c.id AS comment_id, c.content AS comment_content
    FROM POSTS p
    LEFT JOIN COMMENTS c ON p.post_id = c.comment_id
    WHERE p.post_id = ?
    '''
    
    cursor.execute(query, (post_id,))
    
    post = None
    comments = []
    
    for row in cursor.fetchall():
        if post is None:
            post = {
                'post_id': row[3],
                'user_id': row[0],
                'description': row[1],
                'image_url': row[2],
                'comments': []
            }
        
        if row[4] is not None:
            comments.append({
                'comment_id': row[4],
                'comment_content': row[5]
            })
    
    if post:
        post['comments'] = comments
    
    return post
