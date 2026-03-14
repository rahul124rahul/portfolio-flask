#!/usr/bin/env python
"""
Script to create an admin user in the database.
Run this locally with: python create_admin.py
"""
from app import create_app, db
from app.models import Admin

app = create_app()

with app.app_context():
    # Check if admin already exists
    existing_admin = Admin.query.filter_by(username="admin").first()
    if existing_admin:
        print("[OK] Admin user 'admin' already exists!")
        print("  Username: admin")
        exit(0)

    # Create new admin user
    print("Creating admin user...")
    admin = Admin(username="admin", email="admin@portfolio.local")
    admin.set_password("admin123")  # Set default password

    db.session.add(admin)
    db.session.commit()

    print("[OK] Admin user created successfully!")
    print("\n  Username: admin")
    print("  Password: admin123")
    print("\n[!] IMPORTANT: Change these credentials after first login!")
    print("   Visit: https://portfolio-flask-1q00.onrender.com/admin/security")
