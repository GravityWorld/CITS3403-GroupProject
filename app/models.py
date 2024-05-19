from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_login import UserMixin
from app import login


# User model representing a user in the database
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)  # Primary key
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)  # Unique username
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)  # Unique email
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))  # Password hash

    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')  # Relationship to posts

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Method to set password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check password against hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Method to check if the user has liked a specific post
    def has_liked(self, post):
        return Like.query.filter_by(user_id=self.id, post_id=post.id).first() is not None


# Post model representing a post in the database
class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)  # Primary key
    body: so.Mapped[str] = so.mapped_column(sa.String(140))  # Post content
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))  # Timestamp
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)  # Foreign key to User
    author: so.Mapped[User] = so.relationship(back_populates='posts')  # Relationship to User
    tags: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)  # Tags for the post (optional)
    likes = db.relationship('Like', backref='post', lazy='dynamic')  # Relationship to likes

    @property
    def likes_count(self):
        return self.likes.count()  # Property to get the count of likes

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# Like model representing a like in the database
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to User
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # Foreign key to Post

    def __repr__(self):
        return f'<Like user_id={self.user_id} post_id={self.post_id}>'


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))  # Load user by ID
