def connect_to_database(name="database.db"):
    import sqlite3

    return sqlite3.connect(name, check_same_thread=False)


def init_users(connection):
    cursor = connection.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE, 
    password TEXT NOT NULL
    )   
    """
    )

    connection.commit()


def add_user(connection, username, password):
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    cursor.execute(query, (username, password))
    connection.commit()


def get_user_by_username(connection, username):
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchone()


def get_user_by_user_id(connection, user_id):
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()


def init_posts(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS POSTS (
                post_id INTEGER NOT NULL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                date TEXT,
                description TEXT,
                image_data TEXT,
                image_ext TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
    """
    )
    connection.commit()


def add_post(connection, user_id, description, image_data,image_ext, date):
    cursor = connection.cursor()
    query = "INSERT INTO POSTS (user_id, description, image_data , image_ext,date) VALUES(?, ?, ?, ?,?)"
    cursor.execute(query, (user_id, description, image_data,image_ext, date))
    connection.commit()


def get_all_posts(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM POSTS"
    cursor.execute(query)
    posts = list()
    for row in cursor.fetchall():
        post = dict()
        post["post_id"] = row[0]
        post["description"] = row[3]
        post["image_data"] = row[4]
        post["image_ext"] = row[5]
        post["date"] = row[2]
        user_row = get_user_by_user_id(connection, int(row[1]))
        if user_row:
            post["username"] = user_row[1]
        posts.append(post)
    return posts


def init_comments(connection):
    cursor = connection.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS COMMENTS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT not null,
                comment_id INTEGER NOT NULL UNIQUE,
                FOREIGN KEY (comment_id) REFERENCES POSTS (post_id)
            )
    """
    )
    connection.commit()


def add_comment_to_db(connection, user_id, comment_content, comment_id):
    cursor = connection.cursor()
    query = (
        "INSERT INTO COMMENTS (user_id, comment_content, comment_id) VALUES(?, ?, ?)"
    )
    cursor.execute(query, (user_id, comment_content, comment_id))

    connection.commit()


def get_post_by_post_id(connection, post_id):
    cursor = connection.cursor()
    query = "SELECT * FROM POSTS WHERE POST_ID = ?"
    cursor.execute(query, (post_id,))
    post = dict()
    for row in cursor.fetchall():
        post["post_id"] = row[0]
        post["description"] = row[3]
        post["image_data"] = row[4]
        post["image_ext"] = row[5]
        post["date"] = row[2]
        user_row = get_user_by_user_id(connection, int(row[1]))
        if user_row:
            post["username"] = user_row[1]
    return post
