from app import create_app, db
from app.models import Application

app = create_app()

with app.app_context():
    Application.__table__.drop(db.engine)
    Application.__table__.create(db.engine)
    print("✅ Application table reset successfully.")
