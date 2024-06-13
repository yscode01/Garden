from app import app
from models import db, User

def create_admin(username, email, password):
    with app.app_context():
        if User.query.filter_by(username=username).first():
            print(f"User with username '{username}' already exists.")
            return

        if User.query.filter_by(email=email).first():
            print(f"User with email '{email}' already exists.")
            return

        admin_user = User(
            username=username,
            email=email,
            is_admin=True
        )
        admin_user.set_password(password)

        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

if __name__ == "__main__":
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")

    create_admin(username, email, password)
