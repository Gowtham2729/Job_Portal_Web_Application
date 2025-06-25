from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    try:
        num_deleted = User.query.delete()  # Deletes all users from the User table 
        #User.query.filter(User.role != 'admin').delete() --> for deleting non-admin users

        db.session.commit()
        print(f"✅ Deleted {num_deleted} user(s) from the database.")
    except Exception as e:
        print(f"❌ Error: {e}")
