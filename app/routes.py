from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
import humanize
from app import app, db
from app.forms import LoginForm, SignUpForm
from app.models import User
from app.models import Post
from datetime import datetime, timezone
from markupsafe import escape


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
        # If username doesn't exist, proceed with registration
        if form.password.data != form.ReEnterPass.data:
            flash('Error: Passwords do not match', 'error')
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


@app.route('/upload')
def upload():
    if current_user.is_authenticated:
        return render_template("upload.html")
    else:
        # Track the upload intent for anonymous users
        session['upload_intent'] = True
        return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
@login_required
def handle_upload():
    html_content = request.form.get('html')
    css_content = request.form.get('css')
    tags = request.form.get('tags')
    if not html_content.strip():
        flash('Your post is empty.', 'warning')
        return redirect(url_for('display_upload'))

    # Insert the CSS into the HTML content
    if '<head>' in html_content:
        # If there is a <head> tag, add the CSS inside it
        html_content = html_content.replace('<head>', '<head><style>' + css_content + '</style>')
    else:
        # If no <head> tag, prepend a <head> containing the style
        html_content = '<head><style>' + css_content + '</style></head>' + html_content
    

    # Create a new Post instance with the modified HTML content
    #Use of escape to replace symbols for tags with UTF characters in order to isolate css submitted and the page css.
    new_post = Post(body=escape(html_content), author=current_user,tags=tags)
    
    db.session.add(new_post)
    db.session.commit()

    flash('Your HTML has been uploaded successfully!', 'success')
    return redirect(url_for('user_profile', username=current_user.username))

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
    tag_filter = request.args.get('tag')
    sort_order = request.args.get('sort', 'recent')

    posts_query = Post.query

    if tag_filter:
        posts_query = posts_query.filter(Post.tags.contains(tag_filter))

    if sort_order == 'oldest':
        posts_query = posts_query.order_by(Post.timestamp.asc())
    else:  # Default to 'recent'
        posts_query = posts_query.order_by(Post.timestamp.desc())

    top_submissions = posts_query.all()

    for submission in top_submissions:
        # Ensure timestamp is offset-aware
        if submission.timestamp.tzinfo is None:
            submission.timestamp = submission.timestamp.replace(tzinfo=timezone.utc)
        submission.relative_timestamp = humanize.naturaltime(datetime.now(timezone.utc) - submission.timestamp)

    return render_template('gallery.html', title='Hall of Fame', top_submissions=top_submissions)