from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
import humanize
from app import app, db
from app.forms import LoginForm, SignUpForm,UploadForm
from app.models import User, Post, Like
from datetime import datetime, timezone
from markupsafe import escape
import re
from sqlalchemy.orm.exc import NoResultFound



from flask import request, redirect, flash, url_for


from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

@app.route('/')
@app.route('/index')

def index():
    flash('This is a test message.', 'info')

    return render_template('index.html', title='Home')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # Check if there's an upload intent in the session
        upload_intent = session.pop('upload_intent', False)

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')

        # If there was an upload intent, redirect to upload page after login
        if upload_intent:
            return redirect(url_for('upload'))
        else:
            return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        # this checks if the username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Error: Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('signup'))  # redirects back to the registration page and not return external server error
        # Password validation logic
        if form.password.data != form.ReEnterPass.data:
            flash('Error: Passwords do not match', 'error')
            return redirect(url_for('signup'))

        if len(form.password.data) < 8:
            flash('Error: Password must be at least 8 characters long', 'error')
            return redirect(url_for('signup'))

        special_characters = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if not special_characters.search(form.password.data):
            flash('Error: Password must contain at least one special character', 'error')
            return redirect(url_for('signup'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        # If there was an upload intent, redirect to upload page after registration
        if session.get('upload_intent'):
            session.pop('upload_intent')  # Clear the upload intent from session
            login_user(user)
            return redirect(url_for('upload'))
        else:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('signup.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        html_content = form.html.data
        css_content = form.css.data
        tags = form.tags.data

        
        
        if not html_content.strip():
            flash('Your post is empty.', 'warning')
            return redirect(url_for('upload'))
        
        if '<head>' in html_content:
            html_content = html_content.replace('<head>', '<head><style>' + css_content + '</style>')
        else:
            html_content = '<head><style>' + css_content + '</style></head><body>' + html_content + '</body></html>'
        
        # html_content = '<html><head><style>' + css_content + '</style></head><body>' + html_content + '</body></html>'
        new_post = Post(body=escape(html_content), author=current_user, tags=tags)
        db.session.add(new_post)
        db.session.commit()
        
        flash('Your HTML has been uploaded successfully!', 'success')
        return redirect(url_for('user_profile', username=current_user.username))
    
    return render_template('upload.html', form=form)



@app.route('/delete', methods=['GET'])
def delete_post():
    if request.method == 'GET':
        post_id_str = request.args.get('postId')
        if post_id_str:
            try:
                post_id = int(post_id_str)
            except ValueError:
                return "Invalid post ID", 400  # Bad Request
            post = Post.query.get(post_id)
            if post:
                db.session.delete(post)
                db.session.commit()
                return redirect(url_for('user_profile', username=current_user.username))
            else:
                # If post not found
                return "Post not found", 404
        else:
            # If postId parameter is not provided or empty
            return "Post ID is required", 400  # Bad Request

@app.route('/profile')
@login_required
def current_user_profile():
    # Assuming you want to display the profile of the logged-in user
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.timestamp.desc()).all()
    return render_template('profile.html', user=current_user, posts=posts)

@app.route('/profile/<username>')
@login_required
def user_profile(username):
    # This route is for visiting any user's profile by their username
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    return render_template('profile.html', user=current_user, posts=posts)
@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    # Retrieve filter and sort parameters from the request
    tag_filter = request.args.get('tag')
    sort_order = request.args.get('sort', 'recent')

    # Start with a base query for posts
    posts_query = Post.query

    # Apply tag filter if provided
    if tag_filter:
        posts_query = posts_query.filter(Post.tags.contains(tag_filter))

    # Apply sort order based on the provided parameter
    if sort_order == 'oldest':
        # Sort by oldest first
        posts_query = posts_query.order_by(Post.timestamp.asc())
    elif sort_order == 'most_liked':
        # Sort by most liked first
        posts_query = posts_query.outerjoin(Like).group_by(Post.id).order_by(sa.func.count(Like.id).desc())
    else:  # Default to 'recent'
        # Sort by most recent first
        posts_query = posts_query.order_by(Post.timestamp.desc())

    # Execute the query and get the list of posts
    top_submissions = posts_query.all()

    # Process each post for display
    for submission in top_submissions:
        # Ensure timestamp is offset-aware
        if submission.timestamp.tzinfo is None:
            submission.timestamp = submission.timestamp.replace(tzinfo=timezone.utc)
        # Generate a human-readable relative timestamp
        submission.relative_timestamp = humanize.naturaltime(datetime.now(timezone.utc) - submission.timestamp)

    # Render the gallery template with the filtered and sorted posts
    return render_template('gallery.html', title='Hall of Fame', top_submissions=top_submissions)
    
@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    """
    Endpoint to like or unlike a post.

    This endpoint allows the current user to like or unlike a post.
    If the user has already liked the post, it will remove the like (unlike the post).
    If the user has not liked the post, it will add a like to the post.

    :param post_id: ID of the post to like or unlike
    :return: JSON response indicating the action performed ('liked' or 'unliked') and the updated number of likes
    """
    post = Post.query.get_or_404(post_id)  # Retrieve the post or return a 404 error if not found

    if current_user.has_liked(post):  # Check if the current user has already liked the post
        like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()  # Find the like record
        db.session.delete(like)  # Delete the like record
        db.session.commit()  # Commit the transaction
        return jsonify({'result': 'unliked', 'likes': post.likes_count})  # Return the response indicating 'unliked'
    else:
        like = Like(user_id=current_user.id, post_id=post_id)  # Create a new like record
        db.session.add(like)  # Add the like record to the session
        db.session.commit()  # Commit the transaction
        return jsonify({'result': 'liked', 'likes': post.likes_count})  # Return the response indicating 'liked'
