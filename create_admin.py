from werkzeug.security import generate_password_hash

from app import app
from models import db, User


with app.app_context():

    email = "admin@college.com"

    existing = User.query.filter_by(email=email).first()

    if existing:
        print("Administrator already exists.")

    else:

        admin = User(
            name="College Administrator",
            email=email,
            password=generate_password_hash("Admin@123"),
            role="Admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Administrator created successfully.")