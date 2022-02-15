import sqlite3

social_db = sqlite3.connect('social.db')


def add_user(name, email, handle, password):
    """
    Create a user account.
    """
    sql = '''
    INSERT INTO users (name, email, handle, password)
    VALUES (?, ?, ?, ?)
    '''
    social_db.execute(sql, (name, email, handle, password))
    social_db.commit()
    return social_db.lastrowid


def add_friend(user_id, friend_id):
    """
    Add a friend to a user's account.
    """
    sql = '''
    INSERT INTO friends (user_id, friend_id)
    VALUES (?, ?)
    '''
    social_db.execute(sql, (user_id, friend_id))
    social_db.commit()


def add_follower(user_id, follower_id):
    """
    Add a follower to a user's account.
    """
    sql = '''
    INSERT INTO followers (user_id, follower_id)
    VALUES (?, ?)
    '''
    social_db.execute(sql, (user_id, follower_id))
    social_db.commit()


def create_post(user_id, content):
    """
    Create a post for a user.
    """
    sql = '''
    INSERT INTO posts (user_id, content)
    VALUES (?, ?)
    '''
    social_db.execute(sql, (user_id, content))
    social_db.commit()
    return social_db.lastrowid


def create_comment(user_id, post_id, content):
    """
    Create a comment for a post.
    """
    sql = '''
    INSERT INTO comments (user_id, post_id, content)
    VALUES (?, ?, ?)
    '''
    social_db.execute(sql, (user_id, post_id, content))
    social_db.commit()


def display_user_posts(user_id):
    """
    Display the posts for a user.
    """
    sql = '''
    SELECT posts.id, posts.user_id, posts.content, posts.created_at, users.name, users.handle, users.email
    FROM posts
    JOIN users ON posts.user_id = users.id
    WHERE posts.user_id = ?
    ORDER BY posts.created_at DESC
    '''
    return social_db.execute(sql, (user_id,)).fetchall()


def display_comments(post_id):
    """
    Display the comments for a post.
    """
    sql = '''
    SELECT comments.id, comments.user_id, comments.post_id, comments.content, comments.created_at, users.name, users.handle, users.email
    FROM comments
    JOIN users ON comments.user_id = users.id
    WHERE comments.post_id = ?
    ORDER BY comments.created_at DESC
    '''
    return social_db.execute(sql, (post_id,)).fetchall()


def like_post(user_id, post_id):
    """
    Like a post.
    """
    sql = '''
    INSERT INTO likes (user_id, post_id)
    VALUES (?, ?)
    '''
    social_db.execute(sql, (user_id, post_id))
    social_db.commit()


def dislike_post(user_id, post_id):
    """
    Dislike a post.
    """
    sql = '''
    DELETE FROM likes
    WHERE user_id = ? AND post_id = ?
    '''
    social_db.execute(sql, (user_id, post_id))
    social_db.commit()


def display_feed(user_id):
    """
    Display the feed for a user.
    """
    sql = '''
    SELECT posts.id, posts.user_id, posts.content, posts.created_at, users.name, users.handle, users.email
    FROM posts
    JOIN users ON posts.user_id = users.id
    WHERE posts.user_id IN (
        SELECT friend_id
        FROM friends
        WHERE user_id = ?
    )
    OR posts.user_id IN (
        SELECT follower_id
        FROM followers
        WHERE user_id = ?
    )
    OR posts.user_id = ?
    ORDER BY posts.created_at DESC
    '''
    return social_db.execute(sql, (user_id, user_id, user_id)).fetchall()


def switch_feed_oldest(user_id):
    """
    Switch between feeds to prioritize oldest posts.
    """
    sql = '''
    SELECT posts.id, posts.user_id, posts.content, posts.created_at, users.name, users.handle, users.email
    FROM posts
    JOIN users ON posts.user_id = users.id
    WHERE posts.user_id IN (
        SELECT friend_id
        FROM friends
        WHERE user_id = ?
    )
    OR posts.user_id IN (
        SELECT follower_id
        FROM followers
        WHERE user_id = ?
    )
    ORDER BY posts.created_at ASC
    '''
    return social_db.execute(sql, (user_id, user_id)).fetchall()


def switch_feed_controversial(user_id):
    """
    Switch to a controversial feed.
    """
    sql = '''
    SELECT posts.id, posts.user_id, posts.content, posts.created_at, users.name, users.handle, users.email
    FROM posts
    JOIN users ON posts.user_id = users.id
    WHERE posts.user_id IN (
        SELECT friend_id
        FROM friends
        WHERE user_id = ?
    )
    OR posts.user_id IN (
        SELECT follower_id
        FROM followers
        WHERE user_id = ?
    )
    ORDER BY (
        SELECT COUNT(*)
        FROM likes
        WHERE post_id = posts.id
    ) - (
        SELECT COUNT(*)
        FROM likes
        WHERE post_id = posts.id
    ) DESC
    '''
    return social_db.execute(sql, (user_id, user_id)).fetchall()
