import sqlite3

social_db = sqlite3.connect('social.db')


def get_highest_id():
    """
    Get the highest id from the users table.
    """
    sql = '''
    SELECT id
    FROM users
    ORDER BY id DESC
    '''
    return social_db.execute(sql).fetchone()[0]


def add_user(highest_id, name, email, username, password):
    """
    Create a user account.
    """
    sql = '''
    INSERT OR REPLACE INTO users (id, name, email, username, password)
    VALUES (?, ?, ?, ?, ?)
    '''
    social_db.execute(sql, (highest_id, name, email, username, password))
    social_db.commit()


def add_follower(user_id, follower_id):
    """
    Add a follower to a user's account.
    """
    sql = '''
    INSERT OR REPLACE INTO follows (user_id, follower_id)
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


def create_post(id, content, username):
    """
    Create a post for a user.
    """
    sql = '''
    INSERT OR REPLACE INTO posts (id, content, username)
    VALUES (?, ?, ?)
    '''
    social_db.execute(sql, (id, content, username))
    social_db.commit()


def display_user_posts(user_id):
    """
    Display the posts for a user.
    """
    sql = '''
    SELECT posts.id, posts.id, posts.content, posts.created_at, users.name, users.username, users.email
    FROM posts
    JOIN users ON posts.id = users.id
    WHERE posts.id = ?
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
    WHERE id = ?
    '''
    return social_db.execute(sql, (user_id,)).fetchall()


def display_dislikes(user_id):
    """
    Display the dislikes for a user.
    """
    sql = '''
    SELECT dislikes
    FROM posts
    WHERE id = ?
    '''
    return social_db.execute(sql, (user_id,)).fetchall()


def like_post(user_id):
    """
    Like a post.
    """
    sql = '''
    UPDATE posts
    SET likes = likes + 1
    WHERE id = ?
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
    WHERE id = ?
    '''
    social_db.execute(sql, (user_id,))
    social_db.commit()


def display_feed(user_id):
    """
    Display the feed for a user.
    """
    sql = '''
    SELECT posts.id, posts.content, posts.created_at, users.name, users.username, users.email
    FROM posts
    JOIN follows ON follows.follower_id = posts.id
    JOIN users ON users.id = posts.id
    WHERE follows.user_id = ?
    ORDER BY posts.created_at DESC
    '''
    return social_db.execute(sql, (user_id,)).fetchall()


def switch_feed_oldest(user_id):
    """
    Switch between feeds to prioritize oldest posts.
    """
    sql = '''
    SELECT posts.id, posts.id, posts.content, posts.created_at, users.name, users.username, users.email
    FROM posts
    JOIN users ON posts.id = users.id
    WHERE posts.id IN (
        SELECT id
        FROM posts
        WHERE id = ?
    )
    OR posts.id IN (
        SELECT follower_id
        FROM follows
        WHERE id = ?
    )
    ORDER BY posts.created_at ASC
    '''
    return social_db.execute(sql, (user_id, user_id)).fetchall()


def display_feed_other(user_id):
    """
    Display the feed for a user.
    """
    sql = '''
    SELECT posts.id, posts.content, posts.created_at, users.name, users.username, users.email
    FROM posts
    JOIN follows ON follows.follower_id = posts.id
    JOIN users ON users.id = posts.id
    WHERE follows.user_id = ?
    ORDER BY posts.created_at DESC
    '''
    return social_db.execute(sql, (user_id,)).fetchall()


def switch_feed_controversial(user_id):
    """
    Switch to a controversial feed.
    """
    sql = '''
    SELECT id, username, content, created_at, likes, dislikes
    FROM posts
    ORDER BY likes + dislikes DESC
    '''
    return social_db.execute(sql).fetchall()


def get_user_id(username):
    """
    Get user id from username and password.
    """
    sql = '''
    SELECT id
    FROM users
    WHERE username = ?
    '''
    return social_db.execute(sql, (username,)).fetchone()[0]


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


def users_list():
    """
    List all users.
    """
    sql = '''
    SELECT username
    FROM users
    '''
    return social_db.execute(sql).fetchall()


def better_users_list():
    user_list = users_list()
    better_list = []
    for user in user_list:
        better_list.append(user[0])
    return better_list


def main():
    """
    Main function.
    """
    print('Welcome to Social!')
    print('Please log in or create an account.')
    username = input('Username: ')
    password = input('Password: ')
    all_users = better_users_list()
    print(all_users)
    if (username) in all_users:
        user_id = get_user_id(username)
        print(display_feed(user_id))
    else:
        print('Invalid username or password.')
        print('Creating account now')
        name = input('Name: ')
        email = input('Email: ')
        highest_id = social_db.execute(
            'SELECT MAX(id) FROM users').fetchone()[0]
        print("printing highest id" + str(highest_id))
        highest_id = highest_id + 1
        add_user(highest_id, name, email, username, password)
    while True:
        print('What would you like to do?')
        print('1. Create a post')
        print('2. View your posts')
        print('3. View your feed')
        print('4. View your follows')
        print('5. View your likes')
        print('6. Like a post')
        print('7. Dislike a post')
        print('8. Switch to oldest posts')
        print('9. Switch to controversial posts')
        print('10. Follow a user')
        print('11. View a different user\'s feed')
        print('12. Exit')
        choice = input('Choice: ')
        if choice == '1':
            content = input('Content: ')
            create_post(get_user_id(username), content, username)
            print('Post created.')
        elif choice == '2':
            print('Your posts:')
            for post in display_user_posts(get_user_id(username)):
                print('Content:', post[2])
                print('Created at:', post[3])
        elif choice == '3':
            print('Your feed:')
            for post in display_feed(get_user_id(username)):
                print('Post ID:', post[0])
                print('Content:', post[1])
                print('Created at:', post[2])
                print('Poster Name:', post[3])
        elif choice == '4':
            print('Your follows:')
            for user in display_follows(get_user_id(username)):
                print('UserID: ', user[0])
                print('Name: ', user[1])
                print('Username: ', user[2])
        elif choice == '5':
            print('Your like count:')
            print(display_likes(get_user_id(username))[0][0])
            print('Your dislike count:')
            print(display_dislikes(get_user_id(username))[0][0])
        elif choice == '6':
            person = input(
                'Who would you like to like? (enter their username) ')
            like_post(get_user_id(person))
            print('Liked post.')
        elif choice == '7':
            person = input(
                'Who would you like to dislike? (enter their username) ')
            dislike_post(get_user_id(person, password))
            print('Disliked post.')
        elif choice == '8':
            print('Oldest posts:')
            for post in switch_feed_oldest(get_user_id(username)):
                print('User ID:', post[1])
                print('Content:', post[2])
                print('Created at:', post[3])
                print('Name:', post[4])
                print('username:', post[5])
        elif choice == '9':
            print('Controversial posts:')
            for post in switch_feed_controversial(get_user_id(username)):
                print('User ID:', post[1])
                print('Content:', post[2])
                print('Created at:', post[3])
                print('Name:', post[4])
                print('username:', post[5])
        elif choice == '10':
            person = input(
                'Who would you like to follow? (enter their username) ')
            add_follower(get_user_id(username),
                         get_user_id(person))
            print('Followed user.')
        elif choice == '11':
            person = input(
                'Who would you like to view? (enter their username) ')
            print(f'{person}\'s Feed:')
            for post in display_feed(get_user_id(person)):
                print('Post ID:', post[0])
                print('Content:', post[1])
                print('Created at:', post[2])
                print('Poster Name:', post[3])
        elif choice == '12':
            print('Goodbye!')
            return


main()
