from app import app, db
from models import Post, Category, Comment

with app.app_context():
    db.create_all()

    # Add categories
    categories = [
        'Vegetables',
        'Fruits',
        'Herbs',
        'Flowers',
        'Landscaping',
        'Indoor Gardening',
        'Organic Gardening',
        'Garden Tools',
        'Garden Pests',
        'Garden Maintenance'
    ]

    for category_name in categories:
        category = Category(name=category_name)
        db.session.add(category)

    db.session.commit()