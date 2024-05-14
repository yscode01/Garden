from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Post, Category
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db.init_app(app)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Post=Post, Category=Category)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/blog/<post_slug>')
def post(post_slug):
    return render_template('post.html', post_slug=post_slug)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/category/<category_slug>')
def category(category_slug):
    return render_template('category.html', category_slug=category_slug)

@app.route('/tips/<tip_slug>')
def tip(tip_slug):
    return render_template('tip.html', tip_slug=tip_slug)

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        category_id = request.form['category']
        tags = request.form['tags']
        featured_image = request.form['featured_image']

        # Create new post instance
        new_post = Post(title=title, content=content, author=author,
                        category_id=category_id, tags=tags,
                        featured_image=featured_image)

        # Add post to database
        db.session.add(new_post)
        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('home'))

    categories = Category.query.all()
    return render_template('create_post.html', categories=categories)

if __name__ == '__main__':
    app.run(debug=True)