from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)