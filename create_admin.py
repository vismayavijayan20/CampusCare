import os
from getpass import getpass

from app import app
from models import db, User
from werkzeug.security import generate_password_hash


with app.app_context():

    email = os.environ.get("ADMIN_EMAIL", "").strip().lower()

    if not email:
        email = input("Enter administrator email: ").strip().lower()

    existing = User.query.filter_by(email=email).first()

    if existing:
        print("Administrator already exists.")

    else:
        name = input("Enter administrator name: ").strip()
        password = getpass("Enter administrator password: ")
        confirm_password = getpass("Confirm administrator password: ")

        if not name or not email:
            raise ValueError("Name and email are required.")

        if len(password) < 12:
            raise ValueError(
                "Password must contain at least 12 characters."
            )

        if password != confirm_password:
            raise ValueError("Passwords do not match.")

        admin = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role="Admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Administrator created successfully.")