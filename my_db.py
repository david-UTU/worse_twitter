import sqlite3

social_db = sqlite3.connect('social.db')


def add_user(name, email, username, password):
    """
    Create a user account.
    """
    sql = '''
    INSERT INTO users (name, email, username, password)
    VALUES (?, ?, ?, ?)
    '''
    social_db.execute(sql, (name, email, username, password))
    social_db.commit()


def add_follower(user_id, follower_id):
    """
    Add a follower to a user's account.
    """
    sql = '''
    INSERT INTO follows (user_id, follower_id)
    VALUES (?, ?)
    '''
    social_db.execute(sql, (user_id, follower_id))
    social_db.commit()


def display_follows(user_id):
    """
    Display the follows for a user.
    """
    sql = '''
    SELECT users.id, users.name, users.username, users.email
    FROM users
    JOIN follows ON users.id = follows.follower_id
    WHERE follows.user_id = ?
    '''
    return social_db.execute(sql, (user_id,)).fetchall()


def create_post(user_id, content):
    """
    Create a post for a user.
    """
    sql = '''
    UPDATE posts
    SET content = ?
    WHERE user_id = ?
    '''
    social_db.execute(sql, (content, user_id))
    social_db.commit()


def display_user_posts(user_id):
    """
    Display the posts for a user.
    """
    sql = '''
    SELECT posts.id, posts.user_id, posts.content, posts.created_at, users.name, users.username, users.email
    FROM posts
    JOIN users ON posts.user_id = users.id
    WHERE posts.user_id = ?
    ORDER BY posts.created_at DESC
    '''
    return social_db.execute(sql, (user_id,)).fetchall()


def display_likes(user_id):
    """
    Display the likes for a user.
    """
    sql = '''
    SELECT likes
    FROM posts
    WHERE user_id = ?
    '''
    return social_db.execute(sql, (user_id,)).fetchall()


def display_dislikes(user_id):
    """
    Display the dislikes for a user.
    """
    sql = '''
    SELECT dislikes
    FROM posts
    WHERE user_id = ?
    '''
    return social_db.execute(sql, (user_id,)).fetchall()


def like_post(user_id):
    """
    Like a post.
    """
    sql = '''
    UPDATE posts
    SET likes = likes + 1
    WHERE user_id = ?
    '''
    social_db.execute(sql, (user_id,))
    social_db.commit()


def dislike_post(user_id):
    """
    Dislike a post.
    """
    sql = '''
    UPDATE posts
    SET dislikes = dislikes + 1
    WHERE user_id = ?
    '''
    social_db.execute(sql, (user_id,))
    social_db.commit()


def display_feed(user_id):
    """
    Display the feed for a user.
    """
    sql = '''
    SELECT posts.id, posts.user_id, posts.content, posts.created_at, users.name, users.username, users.email
    FROM posts
    JOIN users ON posts.user_id = users.id
    WHERE posts.user_id IN (
        SELECT id
        FROM posts
        WHERE user_id = ?
    )
    OR posts.user_id IN (
        SELECT follower_id
        FROM follows
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
    SELECT posts.id, posts.user_id, posts.content, posts.created_at, users.name, users.username, users.email
    FROM posts
    JOIN users ON posts.user_id = users.id
    WHERE posts.user_id IN (
        SELECT id
        FROM posts
        WHERE user_id = ?
    )
    OR posts.user_id IN (
        SELECT follower_id
        FROM follows
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
    SELECT id, user_id, content, created_at, likes, dislikes
    FROM posts
    ORDER BY likes + dislikes DESC
    '''
    return social_db.execute(sql).fetchall()


def get_user_id(username, password):
    """
    Get user id from username and password.
    """
    sql = '''
    SELECT id
    FROM users
    WHERE username = ? AND password = ?
    '''
    return social_db.execute(sql, (username, password)).fetchone()[0]


def get_post_id(user_id):
    """
    Get post id from user id and content.
    """
    sql = '''
    SELECT id
    FROM posts
    WHERE user_id = ?
    '''
    return social_db.execute(sql, (user_id,)).fetchone()[0]


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
        print('4. View your follows')
        print('5. View your likes')
        print('7. Like a post')
        print('8. Dislike a post')
        print('10. Switch to oldest posts')
        print('11. Switch to controversial posts')
        print('12. Exit')
        choice = input('Choice: ')
        if choice == '1':
            content = input('Content: ')
            create_post(get_user_id(username, password), content)
            print('Post created.')
        elif choice == '2':
            print('Your posts:')
            for post in display_user_posts(get_user_id(username, password)):
                print('ID:', post[1])
                print('Content:', post[2])
                print('Created at:', post[3])
                print('Name:', post[4])
                print('username:', post[5])
        elif choice == '3':
            print('Your feed:')
            for post in display_feed(get_user_id(username, password)):
                print('ID:', post[0])
                print('Content:', post[2])
                print('Created at:', post[3])
                print('Name:', post[4])
                print('username:', post[5])
        elif choice == '4':
            print('Your follows:')
            for user in display_follows(get_user_id(username, password)):
                print('Name:', user[0])
                print('username:', user[1])
                print('Email:', user[2])
        elif choice == '5':
            print('Your likes:')
            print(display_likes(get_user_id(username, password)))
            print('Your dislikes:')
            print(display_dislikes(get_user_id(username, password)))
        elif choice == '7':
            person = input(
                'Who would you like to like? (enter their username) ')
            like_post(get_user_id(person, password))
            print('Liked post.')
        elif choice == '8':
            person = input(
                'Who would you like to dislike? (enter their username) ')
            dislike_post(get_user_id(person, password))
            print('Disliked post.')
        elif choice == '10':
            print('Oldest posts:')
            for post in switch_feed_oldest(get_user_id(username, password)):
                print('ID:', post[0])
                print('User ID:', post[1])
                print('Content:', post[2])
                print('Created at:', post[3])
                print('Name:', post[4])
                print('username:', post[5])
        elif choice == '11':
            print('Controversial posts:')
            for post in switch_feed_controversial(get_user_id(username, password)):
                print('ID:', post[0])
                print('User ID:', post[1])
                print('Content:', post[2])
                print('Created at:', post[3])
                print('Name:', post[4])
                print('username:', post[5])
        elif choice == '12':
            print('Goodbye!')
            return


main()
