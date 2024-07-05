from app import create_app, db
from app.models import User, Role

app = create_app()

with app.app_context():
    db.create_all()

    if not User.query.first():
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('password')
        db.session.add(admin)

        user1 = User(username='user1', email='user1@example.com', role='user')
        user1.set_password('password')
        db.session.add(user1)

        user2 = User(username='user2', email='user2@example.com', role='user')
        user2.set_password('password')
        db.session.add(user2)

        db.session.commit()
        print("Users created.")
    else:
        print("Database already populated.")
