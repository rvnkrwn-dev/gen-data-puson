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


# Function to generate dummy KK data for each user
def generate_kk_data_for_all_users():
    user_data = session.execute(text("SELECT id FROM User")).fetchall()

    if not user_data:
        raise ValueError("No user records found in the database.")

    for user_id_tuple in user_data:
        user_id = user_id_tuple[0]
        number = fake.unique.ean8()
        url_kk = None
        secure_url_kk = None
        public_id_kk = None
        created_at = datetime.now()
        updated_at = datetime.now()
        session.execute(
            text(
                """
                INSERT INTO KK (number, url_kk, secure_url_kk, public_id_kk, user_id, created_at, updated_at) 
                VALUES (:number, :url_kk, :secure_url_kk, :public_id_kk, :user_id, :created_at, :updated_at)
                """
            ),
            {
                "number": number,
                "url_kk": url_kk,
                "secure_url_kk": secure_url_kk,
                "public_id_kk": public_id_kk,
                "user_id": user_id,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )
    session.commit()


# Generate data for all users
generate_kk_data_for_all_users()

# Close the session
session.close()
