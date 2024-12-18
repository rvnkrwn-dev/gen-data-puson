import os
from faker import Faker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from datetime import datetime
import random

# Database configuration
DATABASE_USER = "pusonapp"
DATABASE_PASSWORD = quote_plus("Admin123!")
DATABASE_HOST = "15.235.202.96"
DATABASE_NAME = "pusonapp"

# Set the locale to Indonesian
fake = Faker("id_ID")

# Connect to the database using SQLAlchemy
DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
engine = create_engine(DATABASE_URI, echo=True)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Tambahkan pengecekan untuk memastikan variabel lingkungan diambil dengan benar
if not DATABASE_HOST:
    raise ValueError(
        "DATABASE_HOST tidak diatur. Pastikan variabel lingkungan sudah diatur dengan benar."
    )
if not DATABASE_USER:
    raise ValueError(
        "DATABASE_USER tidak diatur. Pastikan variabel lingkungan sudah diatur dengan benar."
    )
if not DATABASE_PASSWORD:
    raise ValueError(
        "DATABASE_PASSWORD tidak diatur. Pastikan variabel lingkungan sudah diatur dengan benar."
    )
if not DATABASE_NAME:
    raise ValueError(
        "DATABASE_NAME tidak diatur. Pastikan variabel lingkungan sudah diatur dengan benar."
    )

# Roles to assign
roles = ['admin_puskesmas', 'admin_posyandu', 'user']

# Function to generate dummy User data
def generate_user_data(user_count):
    for _ in range(user_count):
        full_name = fake.name()
        email = fake.email()
        password = fake.password()
        url_profile = "http://res.cloudinary.com/dmjb33clr/image/upload/v1733470093/puson_app/profile/avatar.png"
        secure_url_profile = "https://res.cloudinary.com/dmjb33clr/image/upload/v1733470093/puson_app/profile/avatar.png"
        public_id_profile = fake.uuid4()
        role = random.choice(roles)
        status = "pending"
        created_at = datetime.now()
        updated_at = datetime.now()
        session.execute(
            text(
                """
                INSERT INTO User (full_name, email, password, url_profile, secure_url_profile, public_id_profile, role, status, created_at, updated_at) 
                VALUES (:full_name, :email, :password, :url_profile, :secure_url_profile, :public_id_profile, :role, :status, :created_at, :updated_at)
                """
            ),
            {
                "full_name": full_name,
                "email": email,
                "password": password,
                "url_profile": url_profile,
                "secure_url_profile": secure_url_profile,
                "public_id_profile": public_id_profile,
                "role": role,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at
            },
        )
    session.commit()

# Generate data for 100 users
generate_user_data(user_count=100)

# Close the session
session.close()
