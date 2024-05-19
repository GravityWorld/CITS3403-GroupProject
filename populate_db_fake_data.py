from faker import Faker
from app import app, db
from app.models import User, Post, Like
from datetime import datetime, timezone
import random
from markupsafe import escape

# Create an instance of the Faker class
fake = Faker()

def generate_html_post():
    """
    Generate a complete HTML document for a post with a random color applied using inline CSS.
    """
    color = fake.hex_color()
    text = fake.text(max_nb_chars=140)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Post</title>
        <style>*{{color:{color};}}</style>
    </head>
    <body>
        <p>{text}</p>
    </body>
    </html>
    """
    return escape(html_content)

def populate_users(num_users=10):
    """
    Populate the database with fake users.
    """
    with app.app_context():
        for _ in range(num_users):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
            )
            user.set_password(fake.password())
            db.session.add(user)
        db.session.commit()

def populate_posts(num_posts=50):
    """
    Populate the database with fake posts.
    """
    with app.app_context():
        users = User.query.all()
        for _ in range(num_posts):
            post = Post(
                body=generate_html_post(),
                timestamp=fake.date_time_this_year(tzinfo=timezone.utc),
                author=random.choice(users),
                tags=", ".join(fake.words(nb=3))
            )
            db.session.add(post)
        db.session.commit()

def populate_likes(num_likes=100):
    """
    Populate the database with fake likes.
    """
    with app.app_context():
        users = User.query.all()
        posts = Post.query.all()
        for _ in range(num_likes):
            user = random.choice(users)
            post = random.choice(posts)
            like = Like(user_id=user.id, post_id=post.id)
            db.session.add(like)
        db.session.commit()

def add_manual_posts(file_paths):
    """
    Add manual posts from given file paths.
    """
    with app.app_context():
        users = User.query.all()
        for file_path in file_paths:
            with open(file_path, 'r') as file:
                html_content = file.read()
                post = Post(
                    body=escape(html_content),
                    timestamp=datetime.now(timezone.utc),
                    author=random.choice(users),
                    tags=""
                )
                db.session.add(post)
        db.session.commit()

if __name__ == '__main__':
    # Number of users, posts, and likes to create
    NUM_USERS = 10
    NUM_POSTS = 50
    NUM_LIKES = 100

    # File paths for manual posts
    MANUAL_POST_FILES = ['fake_data/post.html', 'fake_data/post2.html']

    # Populate the database
    populate_users(NUM_USERS)
    populate_posts(NUM_POSTS)
    populate_likes(NUM_LIKES)
    
    # Add manual posts
    add_manual_posts(MANUAL_POST_FILES)
    
    print(f'Populated the database with {NUM_USERS} users, {NUM_POSTS} posts, {NUM_LIKES} likes, and manual posts.')
