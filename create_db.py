from app import app, db
from models import Category

with app.app_context():
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
