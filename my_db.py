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


def display_followers(user_id):
    """
    Display the followers for a user.
    """
    sql = '''
    SELECT users.id, users.name, users.handle, users.email
    FROM users
    JOIN followers ON users.id = followers.follower_id
    WHERE followers.user_id = ?
    '''
    return social_db.execute(sql, (user_id,)).fetchall()


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


def display_likes(post_id):
    """
    Display the likes for a post.
    """
    sql = '''
    SELECT likes.user_id, users.name, users.handle, users.email
    FROM likes
    JOIN users ON likes.user_id = users.id
    WHERE likes.post_id = ?
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


def get_user_id(handle, password):
    """
    Get user id from handle and password.
    """
    sql = '''
    SELECT id
    FROM users
    WHERE handle = ? AND password = ?
    '''
    return social_db.execute(sql, (handle, password)).fetchone()[0]


def get_post_id(user_id, content):
    """
    Get post id from user id and content.
    """
    sql = '''
    SELECT id
    FROM posts
    WHERE user_id = ? AND content = ?
    '''
    return social_db.execute(sql, (user_id, content)).fetchone()[0]


def login():
    """
    Login function.
    """
    username = input('Username: ')
    password = input('Password: ')
    user_id = get_user_id(username, password)
    if user_id:
        return display_feed(user_id)
    else:
        print('Invalid username or password.')
        print('Creating account now')
        name = input('Name: ')
        email = input('Email: ')
        add_user(name, email, username, password)
        return display_feed(get_user_id(username, password))


def main():
    """
    Main function.
    """
    print('Welcome to Social!')
    print('Please log in or create an account.')
    username = input('Username: ')
    password = input('Password: ')
    user_id = get_user_id(username, password)
    if user_id:
        print(display_feed(user_id))
    else:
        print('Invalid username or password.')
        print('Creating account now')
        name = input('Name: ')
        email = input('Email: ')
        add_user(name, email, username, password)
        print(display_feed(get_user_id(username, password)))
    while True:
        print('What would you like to do?')
        print('1. Create a post')
        print('2. View your posts')
        print('3. View your feed')
        print('4. View your followers')
        print('5. View your likes')
        print('6. View your comments')
        print('7. Like a post')
        print('8. Dislike a post')
        print('9. Create a comment')
        print('10. Switch to oldest posts')
        print('11. Switch to controversial posts')
        print('12. Exit')
        choice = input('Choice: ')
        if choice == '1':
            content = input('Content: ')
            post_id = create_post(get_user_id(username, password), content)
            print('Post created.')
        elif choice == '2':
            print('Your posts:')
            for post in display_user_posts(get_user_id(username, password)):
                print('ID:', post[0])
                print('Content:', post[2])
                print('Created at:', post[3])
                print('Name:', post[4])
                print('Handle:', post[5])
        elif choice == '3':
            print('Your feed:')
            for post in display_feed(get_user_id(username, password)):
                print('ID:', post[0])
                print('Content:', post[2])
                print('Created at:', post[3])
                print('Name:', post[4])
                print('Handle:', post[5])
        elif choice == '4':
            print('Your followers:')
            for user in display_followers(get_user_id(username, password)):
                print('Name:', user[0])
                print('Handle:', user[1])
                print('Email:', user[2])
        elif choice == '5':
            print('Your likes:')
            for post in display_likes(get_post_id(username, content)):
                print('ID:', post[0])
                print('User ID:', post[1])
                print('Content:', post[2])
                print('Created at:', post[3])
        elif choice == '6':
            print('Your comments:')
            for comment in display_comments(get_post_id(username, content)):
                print('ID:', comment[0])
                print('User ID:', comment[1])
                print('Content:', comment[2])
                print('Created at:', comment[3])
        elif choice == '7':
            post_id = get_post_id(username, content)
            like_post(get_user_id(username, password), post_id)
            print('Liked post.')
        elif choice == '8':
            post_id = get_post_id(username, content)
            dislike_post(get_user_id(username, password), post_id)
            print('Disliked post.')
        elif choice == '9':
            comment_id = create_comment(get_user_id(username, password), get_post_id(
                username, content), input('Comment: '))
            print('Comment created.')
        elif choice == '10':
            print('Oldest posts:')
            for post in switch_feed_oldest(get_user_id(username, password)):
                print('ID:', post[0])
                print('User ID:', post[1])
                print('Content:', post[2])
                print('Created at:', post[3])
                print('Name:', post[4])
                print('Handle:', post[5])
                print('Email:', post[6])
        elif choice == '11':
            print('Controversial posts:')
            for post in switch_feed_controversial(get_user_id(username, password)):
                print('ID:', post[0])
                print('User ID:', post[1])
                print('Content:', post[2])
                print('Created at:', post[3])
                print('Name:', post[4])
                print('Handle:', post[5])
                print('Email:', post[6])
        elif choice == '12':
            print('Goodbye!')
            return
