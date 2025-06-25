from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Check if admin already exists
    if not User.query.filter_by(email='admin@gmail.com').first():
        admin_user = User(
            name='Admin',
            email='admin@gmail.com',
            phone='1234567890',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin user created: admin@gmail.com / admin123")
    else:
        print("⚠️ Admin user already exists.")
    print("✅ Database setup complete.")