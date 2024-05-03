from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, SignUpForm
from app.models import User
from app.models import Post
from datetime import datetime, timezone


@app.route('/')
@app.route('/index')

def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
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
            flash('Error: Username already exists. Please choose a different username.')
            return redirect(url_for('signup'))  # redirects back to the registration page and not return external server error
        # If username doesn't exist, proceed with registration
        if form.password != form.ReEnterPass:
            flash('Error: Passwords do')
            return redirect(url_for('signup'))  # redirects back to the registration page and not return external server error
        if form.password != form.ReEnterPass:
            flash('Error: Passwords do')
            return redirect(url_for('signup'))  # redirects back to the registration page and not return external server error
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('index'))
    return render_template('signup.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/upload')
@login_required
def upload():
    return render_template("upload.html")

@app.route('/upload', methods=['POST'])
@login_required
def handle_upload():
    html_content = request.form.get('html')
    if not html_content.strip():
        flash('Your post is empty.', 'warning')
        return redirect(url_for('display_upload'))

    # Create a new Post instance
    new_post = Post(body=html_content, author=current_user)
    db.session.add(new_post)
    db.session.commit()

    flash('Your HTML has been uploaded successfully!', 'success')
    return redirect(url_for('user_profile',username=current_user.username))

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






@app.route('/gallery')
def hall_of_fame():
    top_submissions = [
        {
            'title': 'Hello World Submission',
            'author': 'User 1',
            'likes': 10,
            'html': """ <div class="card h-100" style="border: 1px solid #ccc; border-radius: 15px; background: linear-gradient(to right, #00c6ff, #0072ff); color: white; text-align: center; padding: 20px; box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);">
  <div class="card-body">
    <h5 class="card-title" style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">Stunning Design</h5>
    <p class="card-text" style="font-size: 16px; margin-bottom: 20px;">This design showcases creativity and skill.</p>
    <div class="content" style="display: flex; justify-content: center;">
      <div class="circle" style="width: 50px; height: 50px; background-color: #fff; border-radius: 50%; margin: 0 10px; animation: pulse 1s infinite alternate;"></div>
      <div class="circle" style="width: 50px; height: 50px; background-color: #fff; border-radius: 50%; margin: 0 10px; animation: pulse 1s infinite alternate;"></div>
      <div class="circle" style="width: 50px; height: 50px; background-color: #fff; border-radius: 50%; margin: 0 10px; animation: pulse 1s infinite alternate;"></div>
    </div>
  </div>
</div>
"""
        },
        {
            'title': 'Submission 2',
            'author': 'User 2',
            'likes': 8,
            'html': """<div class="card h-100" style="border: 1px solid #ccc; border-radius: 15px; background: linear-gradient(to right, #f8f9fa, #f8f9fa); color: #333; text-align: center; padding: 20px; box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);">
  <div class="card-body">
    <h5 class="card-title" style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">Submission Form</h5>
    <form style="display: flex; flex-direction: column; gap: 10px;">
      <label for="title">Title:</label>
      <input type="text" id="title" name="title" style="padding: 5px; border: 1px solid #ccc; border-radius: 5px;">
      
      <label for="author">Author:</label>
      <input type="text" id="author" name="author" style="padding: 5px; border: 1px solid #ccc; border-radius: 5px;">
      
      <label for="html">HTML Code:</label>
      <textarea id="html" name="html" style="padding: 5px; border: 1px solid #ccc; border-radius: 5px; height: 100px;"></textarea>
      
      <button type="submit" style="padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">Submit</button>
    </form>
  </div>
</div>

"""
        },
        # Add more submissions as needed
    ]
    return render_template('gallery.html', title='Hall of Fame', top_submissions=top_submissions)
