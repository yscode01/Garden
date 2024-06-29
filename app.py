from flask import Flask, render_template, request, redirect, url_for, flash, abort
from models import db, User, Post, Category, Comment, Tag
from datetime import datetime
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import os
import logging
from slugify import slugify
from forms import LoginForm, PostForm, CategoryForm, SearchForm
from flask_ckeditor import CKEditor

app = Flask(__name__)
ckeditor = CKEditor(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['DEBUG'] = True
app.config['CKEDITOR_PKG_TYPE'] = 'full'


db.init_app(app)
migrate = Migrate(app, db)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Post=Post, Category=Category)

@app.route('/')
def home():
    app.logger.debug('Home page accessed')
    return render_template('home.html')

@app.route('/blog')
def blog():
    app.logger.debug('Blog page accessed')
    posts = Post.query.all()  # Query for all posts
    return render_template('blog.html', posts=posts)

@app.route('/blog/<post_slug>')
def post(post_slug):
    app.logger.debug(f'Post page accessed: {post_slug}')
    post = Post.query.filter_by(slug=post_slug).first_or_404()
    return render_template('post.html', post=post)

@app.route('/about')
def about():
    app.logger.debug('About page accessed')
    return render_template('about.html')

@app.route('/contact')
def contact():
    app.logger.debug('Contact page accessed')
    return render_template('contact.html')

@app.route('/category/<category_slug>')
def category(category_slug):
    app.logger.debug(f'Category page accessed: {category_slug}')
    category = Category.query.filter_by(slug=category_slug).first_or_404()
    posts = category.posts
    return render_template('category.html', category=category, posts=posts)

@app.route('/tips/<tip_slug>')
def tip(tip_slug):
    app.logger.debug(f'Tip page accessed: {tip_slug}')
    return render_template('tip.html', tip_slug=tip_slug)

@app.route('/journal')
def journal():
    app.logger.debug('Journal page accessed')
    return render_template('journal.html')

@app.route('/resources')
def resources():
    app.logger.debug('Resources page accessed')
    return render_template('resources.html')

@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        tags = form.tags.data.split(',')  # Convert comma-separated string to a list
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            author='admin',  # This should be replaced with the current logged-in user
            date_posted=datetime.utcnow(),
            category_id=form.category.data,
            featured_image=form.featured_image.data,
            status=form.status.data,
            slug=form.title.data.lower().replace(' ', '-'),  # Simple slug generation, improve as needed
            tags=','.join(tags)  # Store the tags as a comma-separated string
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully', 'success')
        return redirect(url_for('home'))
    return render_template('admin/create_post.html', form=form)

@app.route('/blog/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    if not current_user.is_admin:
        abort(403)
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.featured_image = form.featured_image.data
        post.status = form.status.data

        post.slug = slugify(form.title.data)

        category = Category.query.get(form.category.data)
        if category:
            post.category = category

        tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        post.tags = ','.join(tag_names)

        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('post', post_slug=post.slug))

    return render_template('admin/edit_post.html', form=form, post=post)


@app.route('/blog/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    if not current_user.is_admin:
        abort(403)
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully.', 'info')
    return redirect(url_for('blog'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        keywords = form.keywords.data
        category_id = form.category.data
        author = form.author.data
        tags = form.tags.data

        query = Post.query

        if keywords:
            search = f"%{keywords}%"
            query = query.filter((Post.title.ilike(search)) | (Post.content.ilike(search)))

        if category_id:
            query = query.filter_by(category_id=category_id)

        if author:
            query = query.filter(Post.author.ilike(f"%{author}%"))

        if tags:
            search_tags = tags.split(',')
            for tag in search_tags:
                query = query.filter(Post.tags.ilike(f"%{tag.strip()}%"))

        results = query.all()
        return render_template('search_results.html', form=form, results=results)

    return render_template('search.html', form=form)

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)  # Forbidden

    form = CategoryForm()
    categories = Category.query.all()
    posts = Post.query.all()

    return render_template('admin/dashboard.html', posts=posts, form=form, categories=categories)


@app.route('/admin/categories', methods=['GET', 'POST'])
@login_required
def admin_categories():
    if not current_user.is_admin:
        abort(403)

    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, slug=slugify(form.name.data))
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin_categories'))

    categories = Category.query.all()
    posts = Post.query.all()
    return render_template('admin/dashboard.html', categories=categories, form=form, posts=posts)




@app.route('/admin/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    if not current_user.is_admin:
        abort(403)

    form = CategoryForm()

    # Debugging: Log the form data and validation status
    app.logger.debug(f'Form data: {form.data}')
    app.logger.debug(f'Form validation: {form.validate_on_submit()}')

    if form.validate_on_submit():
        app.logger.debug('Form is validated.')

        # Create the new category
        category = Category(name=form.name.data, slug=slugify(form.name.data))
        db.session.add(category)
        db.session.commit()

        app.logger.debug('Category created successfully')
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin_categories'))

    app.logger.debug('Form validation failed or GET request')
    return render_template('admin/new_category.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/admin/category/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if not current_user.is_admin:
        abort(403)

    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = slugify(form.name.data)
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin_categories'))

    return render_template('admin/edit_category.html', form=form, category=category)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
