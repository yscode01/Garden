from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Post, Category
from flask_migrate import Migrate
import os
import logging
from slugify import slugify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24)  # Generates a random secret key
app.config['DEBUG'] = True

db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Set up logging
logging.basicConfig(level=logging.DEBUG)

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

@app.route('/search')
def search():
    app.logger.debug('Search page accessed')
    return render_template('search.html')

@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        category_id = request.form['category']
        tags = request.form.get('tags', '')  # Provide default empty string if not found
        featured_image = request.form.get('featured_image', '')  # Provide default empty string if not found
        status = request.form.get('status', 'draft')  # Default status to 'draft' if not found

        # Generate slug from title
        slug = slugify(title)

        post = Post(
            title=title,
            content=content,
            author=author,
            category_id=category_id,
            tags=tags,
            featured_image=featured_image,
            status=status,
            slug=slug
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog'))

    categories = Category.query.all()
    return render_template('create_post.html', categories=categories)


if __name__ == '__main__':
    app.run(debug=True)
